from __future__ import annotations

from dash import callback, Output, Input, State

from src import layout


@callback(
    Output(layout.history.MODAL, "is_open"),
    Input(layout.header.history_button, "n_clicks"),
    State(layout.history.MODAL, "is_open"),
    config_prevent_initial_callbacks=True
)
def open_backup_modal(_, is_open):
    return not is_open


@callback(
    Output(layout.statistics.SETTINGS, "is_open"),
    Input(layout.statistics.settings_button, "n_clicks"),
    State(layout.statistics.SETTINGS, "is_open"),
    config_prevent_initial_callbacks=True
)
def open_statistics_settings_modal(_, is_open):
    return not is_open
