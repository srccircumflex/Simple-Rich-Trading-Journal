from dash import html, dcc

from src.config import rc

autocdropdown = dcc.Dropdown(
    id="autocdropdown_",
    style={
        "position": "absolute",
        "zIndex": -1,
        "width": 280,

    },
    optionHeight=20,
    maxHeight=rc.gridRow3Height,
    className="autocdropdown"
)

autoctrigger = dcc.Input(id="autoctrigger_", style={"display": "none"})

COMPONENTS = html.Div([
    autocdropdown,
    autoctrigger
])
