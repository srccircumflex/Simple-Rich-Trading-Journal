from dash import clientside_callback, Output, Input

from src import layout
from src.config import rc

clientside_callback(
    """async function (_) {
        logApi = await dash_ag_grid.getApiAsync('logElement')
        
        docRoot = document.documentElement
        gridSplitter = document.getElementById('gridSplitter')
        gridC1 = document.getElementById('gridC1')
        gridC2 = document.getElementById('gridC2')
        gridR1 = document.getElementById('gridR1')
        gridR2 = document.getElementById('gridR2')
        gridR3 = document.getElementById('gridR3')
        bottomBar = document.getElementById('bottomBar')
        dragContainer = document.getElementById('dragContainer')
        dragEventReceiver = document.getElementById('dragEventReceiver')
        editEventReceiver = document.getElementById('editEventReceiver')
        logElement = document.getElementById('logElement')
        autoCDropdown = document.getElementById('autoCDropdown')
        autoCTrigger = document.getElementById('autoCTrigger')
        notepaperContainer = document.getElementById('notepaperContainer')
        notepaperElement = document.getElementById('notepaperElement')
        noteEditorContainer = document.getElementById("noteEditorContainer")
        noteContentPipe = document.getElementById('noteContentPipe')
        noteFileClonePipe = document.getElementById('noteFileClonePipe')
        noteEditorFileRequest = document.getElementById('noteEditorFileRequest')
        noteFileCloneC = document.getElementById('noteFileCloneC')
        
        noteEditor = CodeMirror(noteEditorContainer, {
                lineNumbers: true,
                mode: 'markdown',
                autoCloseBrackets: true,
                matchBrackets: true,
        })
            
        logApi.setFocusedCell(0, 'Name')
        
        make_wingrid()
        make_draggable()
        if (!%d) {
            make_copypaste()
        }
        make_autocomplete()
        make_note(%d)
        
        return window.dash_clientside.no_update
    }""" % (
        rc.disableCopyPaste,
        rc.noteFileDropCloner
    ),
    Output(layout.init_done_trigger, "id"),
    Input(layout.init_done_trigger, "n_clicks"),
)
