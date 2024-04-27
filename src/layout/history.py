import dash_bootstrap_components as dbc
from dash import html, dcc

MODAL = dbc.Modal([
    dbc.ModalHeader([
        dbc.ModalTitle("History")
    ]),
    dbc.ModalBody([
        html.P(
            "Slots are created at startup if the current data differs from the first slot in the history. "
            "Therefore, the time stamps correspond to this startup and not the modification time."
        ),
        html.P(
            "When an slot is selected, `Auto. Save` is automatically deactivated. "
            "If the loaded slot is to be saved as new main data, `Auto. Save` must be activated manually. "
            "Otherwise the page can be reloaded to return to the current main data."
        ),
        html.Hr(),
        history_list := dcc.RadioItems(
            [],
            id="history_list_",
            style={
                "fontFamily": "monospace",
                "fontSize": "13px",
            }
        )
    ])
],
    id="history_modal_",
    scrollable=True,
)
