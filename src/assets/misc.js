if (!window.dash_clientside) {
    window.dash_clientside = {}
    var __setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set
}

function dispatch_event (ele) {
    var client_event = new Event('input', { bubbles: true })
    ele.dispatchEvent(client_event)
}

function setter (ele, val) {
    __setter.call(ele, val)
    var client_event = new Event('input', { bubbles: true })
    dispatch_event(ele)
}

var winWidth = null
var winHeight = null
var isDown = false
var isHover = false
var minWidth = null
var maxWidth = null
var defWidth = null




function c2Hide (doHide) {
    if (doHide % 2) {
        if (gridC1.classList.contains('col-div-flex')) {
            gridC1.classList.remove('col-div-flex')
        }
        gridC1.style.width = winWidth  + 'px'
        if (gridC2.classList.contains('col-div-flex')) {
            gridC2.classList.remove('col-div-flex')
        }
        gridC2.style.width = '0px'
        docRoot.style.setProperty('--handle-x', winWidth + 'px')
    }
    else if (gridC2.clientWidth == 0) {
        if (gridC1.classList.contains('col-div-flex')) {
            gridC1.classList.remove('col-div-flex')
        }
        gridC1.style.width = (winWidth - defWidth)  + 'px'
        if (gridC2.classList.contains('col-div-flex')) {
            gridC2.classList.remove('col-div-flex')
        }
        gridC2.style.width = defWidth + 'px'
        docRoot.style.setProperty('--handle-x', defWidth + 'px')
    }
    return 0
}


function autocomplete (value) {
    if (value) {
        trigger = JSON.parse(autoCTrigger.value)
        if (trigger) {
            if (trigger._eid) {
                cell = document.getElementById(trigger._eid)
                setter(cell, value)
                cell.focus()
            }
            else {
                focCell = logApi.getFocusedCell()
                row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
                row.setDataValue(focCell.column.colId, value)
                logApi.setFocusedCell(trigger._idx, trigger._col)
                // logApi.startEditingCell({"rowIndex": trigger._idx, "colKey": trigger._col})
            }
        }
        autoCDropdown.style.zIndex = -1
    }
    return null
}


function syncColumns (_) {
    function refresh () {
        logApi.refreshCells({force: true, columns: ['Name', 'n', 'InvestTime', 'InvestAmount', 'InvestCourse', 'TakeTime', 'TakeAmount', 'TakeCourse', 'ITC', 'Profit', 'Performance', 'Dividend']})
    }
    refresh()
    setTimeout(refresh, 1)
    return window.dash_clientside.no_update
}


function noteLinkPipe (value) {
    if (value) {
        cursorFrom = noteEditor.getCursor('from')
        cursorTo = noteEditor.getCursor('to')
        noteEditor.replaceRange(value, cursorFrom, cursorTo)
        noteEditor.focus()
        return null
    }
}




async function make_wingrid () {

    bottomBar.addEventListener(
        'mouseout',
        function (e) {
            bottomBar.style.display = "none"
        }
    )
    gridR3.addEventListener(
        'mouseover',
        function (e) {
            bottomBar.style.display = ""
        }
    )

    function resizeGrid () {
        winWidth = (window.innerWidth > 0) ? window.innerWidth : screen.width
        winHeight = (window.innerHeight > 0) ? window.innerHeight : screen.height
        docRoot.style.setProperty('--handle-x', maxWidth + 'px')
        gridR3.style.height = gridRow3Height + 'px'
        gridR2.style.height = (winHeight - gridRow3Height - gridR1.clientHeight) + 'px'
        defWidth = winWidth * gridDefWidthScale
        minWidth = winWidth * gridMinWidthScale
        maxWidth = winWidth - minWidth
        var cl = this.document.querySelector('.col-div')
        if (cl) {
            docRoot.style.setProperty('--handle-x', (cl.offsetWidth) + 'px')
        }
    }
    resizeGrid()
    function moveTo (e) {
        if (e.clientX > minWidth && e.clientX < maxWidth) {
            if (gridC1.classList.contains('col-div-flex')) {
                gridC1.classList.remove('col-div-flex')
            }
            gridC1.style.width = e.clientX  + 'px'
            if (gridC2.classList.contains('col-div-flex')) {
                gridC2.classList.remove('col-div-flex')
            }
            gridC2.style.width = winWidth - e.clientX  + 'px'
            docRoot.style.setProperty('--handle-x', (e.clientX) + 'px')
        }
    }
    window.addEventListener('DOMContentLoaded', function (e) {
        resizeGrid()
    })
    window.addEventListener('resize', function (e) {
        resizeGrid()
    })
    docRoot.addEventListener('mousedown', function (e) {
        if (isHover) {
            isDown = true
        }
    }, true)
    document.addEventListener('mouseup', function (e) {
        isDown = false
        if (isHover) {
            //...
        }
    }, true)
    document.addEventListener('mousemove', function (e) {
        if (isDown) {
            moveTo(e)
        }
    })
    gridSplitter.addEventListener('mouseenter', function (e) {
        isHover = true
        gridSplitter.style.cursor = 'col-resize'
    })
    gridSplitter.addEventListener('mouseout', function (e) {
        isHover = false
    })
    gridSplitter.addEventListener('dblclick', function (e) {
        let defWidth2 = winWidth - defWidth
        let c1W = defWidth
        let c2W = defWidth2

        if ((defWidth * 0.09) <= gridC1.clientWidth && gridC1.clientWidth <= (defWidth * 1.01)) {
            c1W = defWidth2
            c2W = defWidth
        }
        gridC1.style.width = c1W  + 'px'
        gridC2.style.width = c2W  + 'px'
        docRoot.style.setProperty('--handle-x', c1W + 'px')
    })
}


async function make_draggable () {
    dragul = dragula([dragContainer])
    dragul.on("drop", function (el, target, source, sibling) {
        var result = {
            'element': el.id,
            'target_id': target.id,
            'target_children': Array.from(target.children).map(function (child) {return child.id})
        }
        if (source.id != target.id) {
            result['source_id'] = source.id
            result['source_children'] = Array.from(source.children).map(function (child) {return child.id})
        }
        setter(dragEventReceiver, JSON.stringify(result))
    })
}


async function make_copypaste () {

    // fixme: Uncaught (in promise) DOMException: Clipboard write was blocked due to lack of user activation.

    function paste (e) {
        console.log("PASTE: e=", e)
        focCell = logApi.getFocusedCell()
        row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
        value = e.clipboardData.getData('text/plain')
        old_row = JSON.stringify(row.data)
        colId = null
        console.log("PASTE: value=", value)
        if (value.startsWith('{')) {
            value = JSON.parse(value)
            value.id = row.data.id
            row.setData(value)
            new_row = JSON.stringify(value)
        }
        else {
            numCols = ["n", "InvestAmount", "InvestCourse", "TakeAmount", "TakeCourse", "cit"]
            if (numCols.includes(focCell.column.colId)) {
               value = parseFloat(value)
            }
            colId = focCell.column.colId
            row.setDataValue(focCell.column.colId, value)
            row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
            new_row = JSON.stringify(row.data)
        }
        update = {
            "new_row": new_row,
            "old_row": old_row,
            "colId": colId,
        }
        setTimeout(
            function () {
                setter(editEventReceiver, JSON.stringify(update))
            },
            3
        )
    }

    logElement.addEventListener('paste', function (e) {
        console.log("PASTE: EventListener @ ", document.activeElement)
        if (document.activeElement.role == "gridcell") {
            paste(e)
        }
    })

    logElement.addEventListener('keydown', function (e) {
        // console.log("KEYDOWN: e=", e)
        if (e.ctrlKey && e.code == ccCopy) {  // ctrl+c
            e.preventDefault()
            focCell = logApi.getFocusedCell()
            row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
            value = row.data[focCell.column.colId]
            console.log("CLIPBOARD write:", value)
            navigator.clipboard.writeText(value)
            return false
        }
        else if (e.ctrlKey && e.code == ccCut) {  // ctrl[+shift]+x
            e.preventDefault()
            focCell = logApi.getFocusedCell()
            row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
            old_row = JSON.stringify(row.data)
            if (e.shiftKey) {
                value = JSON.stringify(row.data)
                new_row = {"id": row.data.id}
                update = {
                    "new_row": JSON.stringify(new_row),
                    "old_row": old_row,
                }
                row.setData(new_row)
            }
            else {
                value = row.data[focCell.column.colId]
                row.setDataValue(focCell.column.colId, null)
                row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
                update = {
                    "new_row": JSON.stringify(row.data),
                    "old_row": old_row,
                    "colId": focCell.column.colId,
                }
            }
            console.log("CLIPBOARD write:", value)
            navigator.clipboard.writeText(value)
            setter(editEventReceiver, JSON.stringify(update))
            return false
        }
        else if (e.ctrlKey && e.code == ccPaste) { // ctrl+v
        }
        else if ((e.ctrlKey && e.code == ccCopyRow1) || (e.ctrlKey && e.code == ccCopyRow2) || (e.ctrlKey && e.code == ccCopyRow3)) { // ctrl+a || ctrl+y || ctrl+z
            e.preventDefault()
            focCell = logApi.getFocusedCell()
            row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
            value = JSON.stringify(row.data)
            console.log("CLIPBOARD: write", value)
            navigator.clipboard.writeText(value)
            return false
        }
    })
}


async function make_autocomplete () {
    logElement.addEventListener('keydown', function (e) {
        if (e.ctrlKey && e.code == ccAComplete) { // ctrl+<space>
            e.preventDefault()

            focCell = logApi.getFocusedCell()
            row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)

            if (["Name", "Type", "Symbol"].includes(focCell.column.colId)) {

                trigger = JSON.parse(JSON.stringify(row.data))
                trigger._col = focCell.column.colId
                trigger._idx = focCell.rowIndex
                trigger._eid = e.target.id
                setter(autoCTrigger, JSON.stringify(trigger))

                rect = e.target.getBoundingClientRect()
                autoCDropdown.style.top = (rect.top + rect.height) + "px"
                autoCDropdown.style.left = rect.left + "px"
                autoCDropdown.style.zIndex = 20
                autocdropdown_inp = autoCDropdown.children[0].children[0].children[0].children[1].children[0]
                if (e.target.tagName === "INPUT") {
                    setter(autocdropdown_inp, e.target.value)
                } else if (e.target.tagName === "DIV") {
                    setter(autocdropdown_inp, e.target.textContent)
                }
                autocdropdown_inp.focus()
            }
            return false
        }
    })

    function autocexit () {
        trigger = JSON.parse(autoCTrigger.value)
        if (trigger) {
            if (trigger._eid) {
                cell = document.getElementById(trigger._eid)
                if (cell) {
                    setter(cell, cell.value)
                    setTimeout(
                        function () {
                            cell.focus()
                        },
                        3
                    )
                }
            }
            else {
                setTimeout(
                    function () {
                        logApi.setFocusedCell(trigger._idx, trigger._col)
                        // logApi.startEditingCell({"rowIndex": trigger._idx, "colKey": trigger._col})
                    },
                    3
                )
            }
        }
        autoCDropdown.style.zIndex = -1
    }

    autoCDropdown.addEventListener('keydown', function (e) {
        if (e.key === "Escape") {
            e.preventDefault()
            autocexit()
            return false
        }
    })

    autoCDropdown.addEventListener('focusout', function (e) {
        autocexit()
    })
}


async function make_note (fileDropClone) {

    cur_focCell = null
    cur_row = null

    function backtocell() {
        if (cur_focCell) {
            logApi.ensureColumnVisible(cur_focCell)
            logApi.setFocusedCell(cur_focCell.rowIndex, cur_focCell.column.colId)
        }
    }

    function editor_to_cell () {
        if (cur_row) {
            cur_row.setDataValue("Note", noteEditor.getValue())
        }
    }

    if (noteCellVariableFormatter || noteUnifying) {
        function wr_pipe (content) {
            setter(noteContentPipe, JSON.stringify({"content": content, "row": cur_row.data}))
        }
    } else {
        function wr_pipe (content) {
            setter(noteContentPipe, JSON.stringify({"content": content, }))
        }
    }

    function editor_set (value) {
        wr_pipe(value)
        noteEditor.setValue(value)
    }

    function swich () {
        if (noteEditorContainer.style.left == "10px") {
            noteEditorContainer.style.right = "10px"
            noteEditorContainer.style.left = "calc(50% + 10px)"
            notepaperContainer.style.left = "10px"
            notepaperContainer.style.right = "calc(50% + 10px)"
        }
        else {
            notepaperContainer.style.right = "10px"
            notepaperContainer.style.left = "calc(50% + 10px)"
            noteEditorContainer.style.left = "10px"
            noteEditorContainer.style.right = "calc(50% + 10px)"
        }
    }

    noteEditor.on("changes", function (_, e) {
        if (notepaperContainer.style.zIndex == 20) {
            wr_pipe(noteEditor.getValue())
        }
    })
    noteEditor.on('focusout', function (_, e) {editor_to_cell()})
    window.addEventListener('focusout', function (e) {editor_to_cell()})
    window.addEventListener('beforeunload', function (e) {editor_to_cell()})

    logElement.addEventListener('click', function (e) {
        if (notepaperContainer.style.zIndex == 20 || noteEditorContainer.style.zIndex == 20) {
            e.preventDefault()
            focCell = logApi.getFocusedCell()
            _cur_row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
            editor_to_cell()
            cur_focCell = focCell
            cur_row = _cur_row
            editor_set(_cur_row.data["Note"] || "")
            return false
        }
    })

    logElement.addEventListener('keydown', function (e) {
        if ((notepaperContainer.style.zIndex == 20 || noteEditorContainer.style.zIndex == 20) && (e.code == 'ArrowUp' || e.code == 'ArrowDown')) { // ↑||↓
            e.preventDefault()
            focCell = logApi.getFocusedCell()
            _cur_row = logApi.getDisplayedRowAtIndex(focCell.rowIndex)
            editor_to_cell()
            cur_focCell = focCell
            cur_row = _cur_row
            editor_set(_cur_row.data["Note"] || "")
            return false
        }
    })

    window.addEventListener('keydown', function (e) {
        if (e.ctrlKey && e.code == ccNote) { // ctrl+i
            e.preventDefault()

            if (e.shiftKey) {
                if (notepaperContainer.style.zIndex == 20 || noteEditorContainer.style.zIndex == 20) {
                    swich()
                } else {
                    notepaperContainer.style.left = "10px"
                    notepaperContainer.style.right = "calc(50% + 10px)"
                    noteEditorContainer.style.right = "10px"
                    noteEditorContainer.style.left = "calc(50% + 10px)"
                    cur_focCell = logApi.getFocusedCell()
                    cur_row = logApi.getDisplayedRowAtIndex(cur_focCell.rowIndex)
                    editor_set(cur_row.data["Note"] || "")
                    noteEditorContainer.style.zIndex = 20
                    noteEditor.focus()
                }
            } else if (document.activeElement.role == "gridcell" && noteEditorContainer.style.zIndex == 20) {
                noteEditor.focus()
            } else if (notepaperContainer.style.zIndex == -1) {
                if (noteEditorContainer.style.zIndex == -1) {
                    notepaperContainer.style.right = "10px"
                    notepaperContainer.style.left = "calc(50% + 10px)"
                    noteEditorContainer.style.left = "10px"
                    noteEditorContainer.style.right = "calc(50% + 10px)"
                    cur_focCell = logApi.getFocusedCell()
                    cur_row = logApi.getDisplayedRowAtIndex(cur_focCell.rowIndex)
                    editor_set(cur_row.data["Note"] || "")
                }
                wr_pipe(noteEditor.getValue())
                notepaperContainer.style.zIndex = 20
            } else if (noteEditorContainer.style.zIndex == -1) {
                cur_focCell = logApi.getFocusedCell()
                cur_row = logApi.getDisplayedRowAtIndex(cur_focCell.rowIndex)
                editor_set(cur_row.data["Note"] || "")
                swich()
                noteEditorContainer.style.zIndex = 20
                noteEditor.focus()
            } else {
                notepaperContainer.style.zIndex = -1
            }

            return false

        } else if (e.key == "Escape") {
            if (!noteEditorFileRequest.style.display) {
                setter(noteFileCloneC, e.timeStamp.toString())
                return false

            } else if (notepaperContainer.style.zIndex == 20 || noteEditorContainer.style.zIndex == 20) {
                notepaperContainer.style.zIndex = -1
                noteEditorContainer.style.zIndex = -1
                editor_to_cell()
                backtocell()
                return false
            }
        }
    })

    noteEditorContainer.addEventListener('keydown', function (e) {
        if (e.ctrlKey && e.code == ccNoteBack) { // ctrl+#
            e.preventDefault()
            backtocell()
            return false
        }
    })

    function fontsize (e) {
        if (e.shiftKey && e.ctrlKey) {
            e.preventDefault()
            if (e.detail < 0) {
                noteEditorContainer.style.fontSize = (parseInt(noteEditorContainer.style.fontSize) + 1) + "px"
            }
            else {
                noteEditorContainer.style.fontSize = (parseInt(noteEditorContainer.style.fontSize) - 1) + "px"
            }
            noteEditor.refresh()
            return false
        }
    }

    noteEditorContainer.addEventListener('mousewheel', function (e) {
        return fontsize(e)
    })

    noteEditorContainer.addEventListener('DOMMouseScroll', function (e) {
        return fontsize(e)
    })

    if (fileDropClone) {
        noteEditor.on("drop", function (_, e) {
            noteEditor.setCursor(noteEditor.coordsChar({left: e.pageX, top: e.pageY}, "page"))
            e.preventDefault()
            file = e.dataTransfer.files[0]
            if (file) {
                reader = new FileReader()
                reader.onload = function (event) {
                    cursorFrom = noteEditor.getCursor("from")
                    cursorTo = noteEditor.getCursor("to")
                    insert_obj = {
                        "file": "file",
                        "data": event.target.result,
                        "name": file.name,
                        "type": file.type,
                        "ctrl": e.ctrlKey,
                        "shift": e.shiftKey,
                        "time": e.timeStamp
                    }
                    setter(noteFileClonePipe, JSON.stringify(insert_obj))
                }
                reader.readAsDataURL(file)
                return false
            } else {
                text = e.dataTransfer.getData("text")
                if (text) {
                    cursorFrom = noteEditor.getCursor("from")
                    cursorTo = noteEditor.getCursor("to")
                    name = text.match(/[^\/|\\]*$/)
                    if (!name) {
                        name = text
                    }
                    if (text.match(noteLinkDropPattern)) {
                        file = "link"
                        if (!text.match(/^\w+:/)) {
                            text = "http://" + text
                        }
                    } else if (text.match(notePathDropPattern)) {
                        file = "path"
                        if (!text.match(/^file:/)) {
                            text = "file:///" + text
                        }
                    } else {
                        file = false
                    }
                    insert_obj = {
                        "file": file,
                        "data": text,
                        "name": name,
                        "time": e.timeStamp
                    }
                    setter(noteFileClonePipe, JSON.stringify(insert_obj))
                    return false
                }
            }
        })
    }
}
