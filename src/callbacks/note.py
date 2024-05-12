from __future__ import annotations

import json
from base64 import b64decode
from os import listdir
from re import sub, DOTALL
from urllib.parse import quote

from dash import callback, Output, Input, State, no_update

from src import layout, FILE_CLONES, FILE_CLONES_URL
from src.config import rc


if rc.noteCellVariableFormatter:
    from string import Formatter

    class _Formatter(Formatter):
        def __init__(self, missing='{??}', bad_fmt='{!!}'):
            self.missing = missing
            self.bad_fmt = bad_fmt

        def get_field(self, field_name, args, kwargs):
            try:
                val = super().get_field(field_name, args, kwargs)
            except (KeyError, AttributeError, IndexError):
                val = None, field_name
            return val

        def format_field(self, value, spec):
            if value is None:
                return self.missing
            try:
                return super().format_field(value, spec)
            except ValueError:
                return self.bad_fmt

        def format(self, __format_string, kwargs):
            try:
                return self.vformat(__format_string, (), kwargs)
            except ValueError as e:
                return f"# **{e.__class__.__name__}**\n\n## _{e}_"


    _formatter = _Formatter()

    def _format(__content, __row):
        return _formatter.format(
            __content,
            {
                  "cat": "N/A",
                  "Name": "N/A",
                  "Symbol": "N/A",
                  "Type": "N/A",
                  "n": "N/A",
                  "InvestTime": "N/A",
                  "InvestAmount": "N/A",
                  "InvestCourse": "N/A",
                  "TakeTime": "N/A",
                  "TakeAmount": "N/A",
                  "TakeCourse": "N/A",
                  "ITC": "N/A",
                  "Performance": "N/A",
                  "Profit": "N/A",
                  "Dividend": "N/A",
                  "Note": "N/A",
                  "HoldTime": "N/A",
                  "Performance/Day": "N/A",
                  "Profit/Day": "N/A",
              } | __row
        )
    if rc.noteMathJax and rc.noteMathJaxMasker:

        def content(obj):
            _content = sub("\\$\\$.*?\\$\\$", lambda m: m.group().replace("{", "{{").replace("}", "}}"), obj["content"], flags=DOTALL)
            return _format(_content, obj["row"])

    else:
        def content(obj):
            return _format(obj["content"], obj["row"])

else:
    def content(obj):
        return obj["content"]


if rc.noteUnifying:

    @callback(
        Output(layout.note.notepaper, "children"),
        Output(layout.note.noteContentPipe, "value"),
        Input(layout.note.noteContentPipe, "value"),
        State(layout.log.tradinglog, "rowData"),
        config_prevent_initial_callbacks=True
    )
    def noteContentPipe(obj, row_data):
        if obj:
            obj = json.loads(obj)
            _content = content(obj)
            _id = obj["row"]["id"]
            if _name := obj["row"].get("Name"):
                for i in range(len(row_data)):
                    if row_data[i]["id"] == _id:
                        for row in row_data[i + 1:]:
                            if row.get("Name") == _name:
                                _content += content({"content": row.get("Note") or "", "row": row})
                        break
            return _content, None
        else:
            return "", None
else:
    @callback(
        Output(layout.note.notepaper, "children"),
        Output(layout.note.noteContentPipe, "value"),
        Input(layout.note.noteContentPipe, "value"),
        config_prevent_initial_callbacks=True
    )
    def noteContentPipe(obj):
        if obj:
            obj = json.loads(obj)
            return content(obj), None
        else:
            return "", None


def make_filelink(
        drop_obj,
        clone=True
):
    if drop_obj["file"] == "file":
        link_name = quote(drop_obj["name"])
        if drop_obj["type"].startswith("image/"):
            if rc.noteFileDropClonerImgAltName:
                name = drop_obj["name"]
            else:
                name = ""
            link = f"![{name}]({FILE_CLONES_URL}/{link_name})"
        else:
            link = f"[{drop_obj['name']}]({FILE_CLONES_URL}/{link_name})"
        if clone:
            header, encoded = drop_obj["data"].split(",", 1)
            data = b64decode(encoded)
            with open(f"{FILE_CLONES}/{drop_obj['name']}", "wb") as f:
                f.write(data)
    elif drop_obj["file"] in ("link", "path"):
        link = f"[{drop_obj['name']}]({drop_obj['data']})"
    else:
        link = drop_obj['data']
    return link


@callback(
    Output(layout.note.noteLinkPipe, "value", allow_duplicate=True),
    Output(layout.note.noteEditorFileRequest, "style", allow_duplicate=True),
    Output(layout.note.noteeditor_file_request_msg, "children"),
    Output(layout.note.noteeditor_file_request_rnto, "children"),
    Output(layout.note.noteFileClonePipe, "value", allow_duplicate=True),
    Input(layout.note.noteFileClonePipe, "value"),
    State(layout.note.noteEditorFileRequest, "style"),
    config_prevent_initial_callbacks=True
)
def fileClone(obj, style):
    if obj:
        obj = json.loads(obj)
        err_rnto = no_update
        err_msg = no_update
        file_pipe = no_update

        name = obj["name"]
        dirlist = listdir(FILE_CLONES)

        if name in dirlist:

            def new_name():
                i = 2
                while (_name := f"{name}-{i}") in dirlist:
                    i += 1
                return _name

            if obj["ctrl"]:
                link = make_filelink(obj, clone=obj["shift"])
                style = no_update
                file_pipe = None
            elif obj["shift"]:
                obj["name"] = new_name()
                link = make_filelink(obj)
                style = no_update
                file_pipe = None
            else:
                link = no_update
                style |= {"display": ""}
                err_msg = name
                err_rnto = new_name()
        else:
            link = make_filelink(obj)
            style = no_update
            file_pipe = None
        return link, style, err_msg, err_rnto, file_pipe
    else:
        return no_update


@callback(
    Output(layout.note.noteLinkPipe, "value", allow_duplicate=True),
    Output(layout.note.noteEditorFileRequest, "style", allow_duplicate=True),
    Output(layout.note.noteFileClonePipe, "value", allow_duplicate=True),
    State(layout.note.noteFileClonePipe, "value"),
    State(layout.note.noteeditor_file_request_rnto, "children"),
    Input(layout.note.noteeditor_file_request_rn, "n_clicks"),
    State(layout.note.noteEditorFileRequest, "style"),
    config_prevent_initial_callbacks=True
)
def fileCloneRN(obj, rnto, rn, style):
    obj = json.loads(obj)
    obj["name"] = rnto
    return make_filelink(obj), style | {"display": "none"}, None


@callback(
    Output(layout.note.noteLinkPipe, "value", allow_duplicate=True),
    Output(layout.note.noteEditorFileRequest, "style", allow_duplicate=True),
    Output(layout.note.noteFileClonePipe, "value", allow_duplicate=True),
    State(layout.note.noteFileClonePipe, "value"),
    Input(layout.note.noteeditor_file_request_ow, "n_clicks"),
    State(layout.note.noteEditorFileRequest, "style"),
    config_prevent_initial_callbacks=True
)
def fileCloneOW(obj, ow, style):
    obj = json.loads(obj)
    return make_filelink(obj), style | {"display": "none"}, None


@callback(
    Output(layout.note.noteLinkPipe, "value", allow_duplicate=True),
    Output(layout.note.noteEditorFileRequest, "style", allow_duplicate=True),
    Output(layout.note.noteFileClonePipe, "value", allow_duplicate=True),
    State(layout.note.noteFileClonePipe, "value"),
    State(layout.note.noteEditorFileRequest, "style"),
    Input(layout.note.noteeditor_file_request_ig, "n_clicks"),
    config_prevent_initial_callbacks=True
)
def fileCloneIG(obj, style, _):
    if obj:
        obj = json.loads(obj)
        return make_filelink(obj, clone=False), style | {"display": "none"}, None
    else:
        return no_update


@callback(
    Output(layout.note.noteLinkPipe, "value", allow_duplicate=True),
    Output(layout.note.noteEditorFileRequest, "style", allow_duplicate=True),
    Output(layout.note.noteFileClonePipe, "value", allow_duplicate=True),
    State(layout.note.noteEditorFileRequest, "style"),
    Input(layout.note.noteFileCloneC, "value"),
    config_prevent_initial_callbacks=True
)
def fileCloneC(style, _):
    return None, style | {"display": "none"}, None