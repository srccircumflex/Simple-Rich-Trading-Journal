if (!window.dash_clientside) {
    window.dash_clientside = {}
    var __setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set
}

function setter (ele, val) {
    __setter.call(ele, val)
    var client_event = new Event('input', { bubbles: true })
    ele.dispatchEvent(client_event)
}

let root = null
let spliter = null
let c1 = null
let c2 = null
let r1 = null
let r2 = null
let r3 = null
let bb = null
let winWidth = null
let winHeight = null
var isDown = false
var isHover = false
var minWidth = null
var maxWidth = null
var defWidth = null


window.dash_clientside.clientside = {
    c2Hide: function (doHide) {
        root = document.documentElement
        c1 = document.getElementById('c-1')
        c2 = document.getElementById('c-2')
        if (doHide % 2) {
            if (c1.classList.contains('col-div-flex')) {
                c1.classList.remove('col-div-flex')
            }
            c1.style.width = winWidth  + 'px'
            if (c2.classList.contains('col-div-flex')) {
                c2.classList.remove('col-div-flex')
            }
            c2.style.width = '0px'
            root.style.setProperty('--handle-x', winWidth + 'px')
        }
        else if (c2.clientWidth == 0) {
            if (c1.classList.contains('col-div-flex')) {
                c1.classList.remove('col-div-flex')
            }
            c1.style.width = (winWidth - defWidth)  + 'px'
            if (c2.classList.contains('col-div-flex')) {
                c2.classList.remove('col-div-flex')
            }
            c2.style.width = defWidth + 'px'
            root.style.setProperty('--handle-x', defWidth + 'px')
        }
        return 0
    },
    make_wingrid: function () {
        setTimeout(
            function () {
                root = document.documentElement
                spliter = document.getElementById('split-handle')
                c1 = document.getElementById('c-1')
                c2 = document.getElementById('c-2')
                r1 = document.getElementById('r-1')
                r2 = document.getElementById('r-2')
                r3 = document.getElementById('r-3')
                bb = document.getElementById('bb')

                bb.addEventListener(
                    'mouseout',
                    function (e) {
                        bb.style.display = "none"
                    }
                )
                r3.addEventListener(
                    'mouseover',
                    function (e) {
                        bb.style.display = ""
                    }
                )

                function resizeGrid () {
                    winWidth = (window.innerWidth > 0) ? window.innerWidth : screen.width
                    winHeight = (window.innerHeight > 0) ? window.innerHeight : screen.height
                    root.style.setProperty('--handle-x', maxWidth + 'px')
                    r3.style.height = gridRow3Height + 'px'
                    r2.style.height = (winHeight - gridRow3Height - r1.clientHeight) + 'px'
                    defWidth = winWidth * gridDefWidthScale
                    minWidth = winWidth * gridMinWidthScale
                    maxWidth = winWidth - minWidth
                    var cl = this.document.querySelector('.col-div')
                    if (cl) {
                        root.style.setProperty('--handle-x', (cl.offsetWidth) + 'px')
                    }
                }
                resizeGrid()
                function moveTo (e) {
                    if (e.clientX > minWidth && e.clientX < maxWidth) {
                        if (c1.classList.contains('col-div-flex')) {
                            c1.classList.remove('col-div-flex')
                        }
                        c1.style.width = e.clientX  + 'px'
                        if (c2.classList.contains('col-div-flex')) {
                            c2.classList.remove('col-div-flex')
                        }
                        c2.style.width = winWidth - e.clientX  + 'px'
                        root.style.setProperty('--handle-x', (e.clientX) + 'px')
                    }
                }
                window.addEventListener('DOMContentLoaded', function (e) {
                    resizeGrid()
                })
                window.addEventListener('resize', function (e) {
                    resizeGrid()
                })
                root.addEventListener('mousedown', function (e) {
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
                spliter.addEventListener('mouseenter', function (e) {
                    isHover = true
                    spliter.style.cursor = 'col-resize'
                })
                spliter.addEventListener('mouseout', function (e) {
                    isHover = false
                })
                spliter.addEventListener('dblclick', function (e) {
                    let defWidth2 = winWidth - defWidth
                    let c1W = defWidth
                    let c2W = defWidth2

                    if ((defWidth * 0.09) <= c1.clientWidth && c1.clientWidth <= (defWidth * 1.01)) {
                        c1W = defWidth2
                        c2W = defWidth
                    }
                    c1.style.width = c1W  + 'px'
                    c2.style.width = c2W  + 'px'
                    root.style.setProperty('--handle-x', c1W + 'px')
                })
            },
            2
        )

        return window.dash_clientside.no_update
    },
    make_draggable: function () {
        setTimeout(
            function () {
                dragul = dragula([document.getElementById('drag_container_')])
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
                    var drag_event_receiver = document.getElementById("drag_event_receiver_")
                    setter(drag_event_receiver, JSON.stringify(result))
                })
            },
            1
        )
        return window.dash_clientside.no_update
    },
    make_copypaste: function () {
        setTimeout(
            async function () {

                // fixme: Uncaught (in promise) DOMException: Clipboard write was blocked due to lack of user activation.

                gridApi = await dash_ag_grid.getApiAsync('tradinglog_')
                tradinglog = document.getElementById('tradinglog_')

                function paste (e) {
                    console.log("PASTE: e=", e)
                    focCell = gridApi.getFocusedCell()
                    row = gridApi.getDisplayedRowAtIndex(focCell.rowIndex)
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
                        row = gridApi.getDisplayedRowAtIndex(focCell.rowIndex)
                        new_row = JSON.stringify(row.data)
                    }
                    update = {
                        "new_row": new_row,
                        "old_row": old_row,
                        "colId": colId,
                    }
                    setTimeout(
                        function () {
                            var edit_event_receiver = document.getElementById("edit_event_receiver_")
                            setter(edit_event_receiver, JSON.stringify(update))
                        },
                        3
                    )
                }

                tradinglog.addEventListener('paste', function (e) {
                    console.log("PASTE: EventListener")
                    paste(e)
                })

                tradinglog.addEventListener('keydown', function (e) {
                    // console.log("KEYDOWN: e=", e)
                    if (e.ctrlKey && e.keyCode == 67) {  // ctrl+c
                        focCell = gridApi.getFocusedCell()
                        row = gridApi.getDisplayedRowAtIndex(focCell.rowIndex)
                        value = row.data[focCell.column.colId]
                        console.log("CLIPBOARD: write", value)
                        navigator.clipboard.writeText(value)
                    }
                    else if (e.ctrlKey && e.keyCode == 88) {  // ctrl[+shift]+x
                        focCell = gridApi.getFocusedCell()
                        row = gridApi.getDisplayedRowAtIndex(focCell.rowIndex)
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
                            row = gridApi.getDisplayedRowAtIndex(focCell.rowIndex)
                            update = {
                                "new_row": JSON.stringify(row.data),
                                "old_row": old_row,
                                "colId": focCell.column.colId,
                            }
                        }
                        console.log("CLIPBOARD: write", value)
                        navigator.clipboard.writeText(value)
                        var edit_event_receiver = document.getElementById("edit_event_receiver_")
                        setter(edit_event_receiver, JSON.stringify(update))
                    }
                    else if (e.ctrlKey && e.keyCode == 86) { // ctrl+v
                    }
                    else if ((e.ctrlKey && e.keyCode == 65) || (e.ctrlKey && e.keyCode == 89) || (e.ctrlKey && e.keyCode == 90)) { // ctrl+a || ctrl+y || ctrl+z
                        focCell = gridApi.getFocusedCell()
                        row = gridApi.getDisplayedRowAtIndex(focCell.rowIndex)
                        value = JSON.stringify(row.data)
                        console.log("CLIPBOARD: write", value)
                        navigator.clipboard.writeText(value)
                    }
                })
            },
            3
        )
        return window.dash_clientside.no_update
    },
    make_autocomplete: function () {
        setTimeout(
            async function () {
                gridApi = await dash_ag_grid.getApiAsync('tradinglog_')
                autocdropdown = document.getElementById('autocdropdown_')
                autoctrigger = document.getElementById("autoctrigger_")
                tradinglog = document.getElementById('tradinglog_')

                tradinglog.addEventListener('keydown', function (e) {
                    if (e.ctrlKey && e.keyCode == 32) { // ctrl+<space>

                        focCell = gridApi.getFocusedCell()
                        row = gridApi.getDisplayedRowAtIndex(focCell.rowIndex)

                        if (["Name", "Type", "Symbol"].includes(focCell.column.colId)) {

                            trigger = JSON.parse(JSON.stringify(row.data))
                            trigger._col = focCell.column.colId
                            trigger._idx = focCell.rowIndex
                            trigger._eid = e.target.id
                            setter(autoctrigger, JSON.stringify(trigger))

                            rect = e.target.getBoundingClientRect()
                            autocdropdown.style.top = (rect.top + rect.height) + "px"
                            autocdropdown.style.left = rect.left + "px"
                            autocdropdown.style.zIndex = 2
                            autocdropdown_inp = autocdropdown.children[0].children[0].children[0].children[1].children[0]
                            if (e.target.tagName === "INPUT") {
                                setter(autocdropdown_inp, e.target.value)
                            } else if (e.target.tagName === "DIV") {
                                setter(autocdropdown_inp, e.target.textContent)
                            }
                            autocdropdown_inp.focus()
                        }
                    }
                })

                function autocexit () {
                    trigger = JSON.parse(autoctrigger.value)
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
                                    gridApi.startEditingCell({"rowIndex": trigger._idx, "colKey": trigger._col})
                                },
                                3
                            )
                        }
                    }
                    autocdropdown.style.zIndex = -1
                }

                autocdropdown.addEventListener('keydown', function (e) {
                    if (e.key === "Escape") {
                        autocexit()
                    }
                })

                autocdropdown.addEventListener('focusout', function (e) {
                    autocexit()
                })
            },
            1
        )
        return window.dash_clientside.no_update
    },
    autocomplete: async function (value) {
        if (value) {
            gridApi = await dash_ag_grid.getApiAsync('tradinglog_')
            autoctrigger = document.getElementById('autoctrigger_')
            trigger = JSON.parse(autoctrigger.value)
            if (trigger) {
                if (trigger._eid) {
                    cell = document.getElementById(trigger._eid)
                    setter(cell, value)
                    cell.focus()
                }
                else {
                    focCell = gridApi.getFocusedCell()
                    row = gridApi.getDisplayedRowAtIndex(focCell.rowIndex)
                    row.setDataValue(focCell.column.colId, value)
                    gridApi.startEditingCell({"rowIndex": trigger._idx, "colKey": trigger._col})
                }
            }
            autocdropdown = document.getElementById('autocdropdown_')
            autocdropdown.style.zIndex = -1
        }
    }
}