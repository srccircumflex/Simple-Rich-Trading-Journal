from dash import clientside_callback, Output, Input

from src import layout
from src.config import rc

clientside_callback(
    """function (_) {
        window.dash_clientside.clientside.make_wingrid();
        window.dash_clientside.clientside.make_draggable();
        if (!%d) {
            window.dash_clientside.clientside.make_copypaste();
        }
        window.dash_clientside.clientside.make_autocomplete();
        return window.dash_clientside.no_update
    }""" % rc.disableCopyPaste,
    # ClientsideFunction(namespace="clientside", function_name="make"),
    Output(layout.c_1, "id"),
    Input(layout.c_1, "id"),
)
