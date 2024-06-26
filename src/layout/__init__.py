import dash_bootstrap_components as dbc
from dash import html

from src.config import styles, rc, color_theme
from src.layout import header, history, statistics, balance, autocomplet, note
from src.layout import make
from src.layout.log import tradinglog

LAYOUT = html.Div(
    [
        html.Header(
            [
                html.Meta(name="viewport", content="width=device-width, initial-scale=1.0")
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            html.Div(
                                                [
                                                    header.scopes_check,
                                                    header.search_input,
                                                    header.daterange,
                                                    header.index_by_button,
                                                    header.scope_by_button,
                                                    html.Div(style={"display": "inline-block", "width": "1%"}),
                                                    header.with_open_button,
                                                    header.with_open_trigger,
                                                ],
                                                style={
                                                    "display": "flex"
                                                }
                                            ),
                                            style={
                                                "width": "100%",
                                                "display": "inline-block"
                                            }
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        header.auto_save_button,
                                                        header.update_interval_button,
                                                        header.update_interval_button_trigger,
                                                        header.update_interval,
                                                        header.update_interval_trigger,
                                                    ],
                                                    style={
                                                        "textAlign": "end",
                                                    }
                                                ),
                                            ],
                                            style={
                                                "position": "absolute",
                                                "top": 0,
                                                "right": 0,
                                                "textAlign": "end",
                                            }
                                        ),
                                    ],
                                    style={
                                              "width": "100%",
                                              "display": "flex"
                                          } | styles.misc.header
                                ),
                            ],
                            id="gridR1"
                        ),
                        html.Div(
                            [
                                c_1 := html.Div(
                                    [
                                        tradinglog,
                                    ],
                                    id="gridC1",
                                    className="col-div col-div-flex border-div",
                                    style={
                                        "width": rc.c1Width,
                                        "height": "100%"
                                    }
                                ),
                                split_handle := html.Div(
                                    id="gridSplitter",
                                    style={
                                              "height": "inherit",
                                          } | (styles.misc.balance_split_handle if rc.sideInitBalance else styles.misc.statistics_split_handle),
                                    className="noselect"
                                ),
                                c_2 := html.Div(
                                    [
                                        statistics.STATISTICS,
                                        balance.BALANCE
                                    ],
                                    id="gridC2",
                                    className="col-div col-div-flex border-div",
                                    style={
                                        "width": rc.c2Width,
                                        "height": "100%",
                                    }
                                )
                            ],
                            id="gridR2",
                            style={
                                "display": "flex"
                            }
                        )
                    ]
                ),
            ],
            style={
                "backgroundColor": color_theme.table_bg_main
            }
        ),
        html.Div(
            [
                renderer_trigger := html.Div(id="style_trigger_", n_clicks=0),
                c2Hide_trigger := html.Div(id="c2Hide_trigger_", n_clicks=0),
                drag_event_receiver := dbc.Input(type="text", id="dragEventReceiver", style={'visibility': 'hidden', "display": "none"}),
                edit_event_receiver := dbc.Input(type="text", id="editEventReceiver", style={'visibility': 'hidden', "display": "none"}),
                history.MODAL,
                statistics.POP,
                statistics.SETTINGS,
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(style={"display": "inline-block", "width": "1%"}),
                        header.reload_button,
                        header.history_button,
                        header.import_button,
                        header.export_button,
                    ],
                    style={
                        "width": "50%",
                        "textAlign": "left",
                        "display": "inline-block"
                    }
                ),
                html.Div(
                    [
                        header.balance_button,
                        header.statistics_button,
                    ],
                    style={
                        "width": "50%",
                        "textAlign": "right",
                        "display": "inline-block"
                    }
                ),
            ],
            id="bottomBar",
            style={
                "position": "absolute",
                "bottom": rc.bottomBarDistanceBottom,
                "right": rc.bottomBarDistanceRight,
                "width": "100%",
                "zIndex": 1,
                "display": "none"
            }
        ),
        summary_footer := html.Div(
            id="gridR3",
            style={
                "width": "100%",
                "position": "absolute",
                "bottom": 0,
            } | styles.misc.summary_footer
        ),
        (html.Div(
            rc.profile_name,
            style={
                "position": "absolute",
                "bottom": 0,
                "left": 0,
                "fontSize": 12,
                "borderTop": "2px outset",
                "borderRight": "2px outset",
                "paddingLeft": 3,
                "paddingRight": 4,
            } | styles.misc.summary_footer | {"backgroundColor": ""}
        ) if rc.profile_name else html.Div()),
        init_trigger := html.Div(id="init_trigger_"),
        init_done_trigger := html.Div(id="init_done_trigger_"),
        autocomplet.COMPONENTS,
        note.COMPONENTS,
    ]
)
