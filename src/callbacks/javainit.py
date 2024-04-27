from dash import clientside_callback, ClientsideFunction, Output, Input

from src import layout

clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="make"),
    Output(layout.c_1, "id"),
    Input(layout.c_1, "id"),
)
