import dash_bootstrap_components as dbc
from dash import html, dcc

from src.config import styles, rc
from src.config.functional import performance_trailing

SETTINGS = dbc.Modal([
    dbc.ModalBody(
        [
            html.Div(
                [
                    performance_range := dcc.Dropdown(
                        options=performance_trailing.performance_range,
                        value=performance_trailing.performance_range_default,
                        style={"width": "100%"},
                        id="performance_range_"),
                    performance_steps := dcc.Dropdown(
                        options=performance_trailing.performance_steps,
                        value=performance_trailing.performance_steps_default,
                        style={"width": "100%"},
                        id="performance_steps_"),
                    performance_trailing_frame := dcc.Dropdown(
                        options=performance_trailing.performance_frame,
                        value=performance_trailing.performance_frame_default,
                        style={"width": "100%"},
                        id="performance_trailing_frame_"),
                    performance_trailing_interval := dcc.Dropdown(
                        options=performance_trailing.performance_interval,
                        value=performance_trailing.performance_interval_default,
                        style={"width": "100%"},
                        id="performance_trailing_interval_"),
                ],
                style={
                    "fontSize": "13px"
                }
            ),
        ]
    )
],
    id="statistic_settings_modal_",
    size="xs",
    scrollable=True,
)

POP = dbc.Modal([
    dbc.ModalHeader([
        html.Div([
            pop_title := html.H4(id="pop_title_", style={"display": "inline-block", "width": "15%"}),
            html.Div(
                pop_size_slider := dcc.Slider(**styles.figures.size_slider_kwargs_pop, id="pop_size_slider_"),
                style={"display": "inline-block", "width": "85%"}
            )
        ],
            style={"width": "100%", "display": "flex"}
        )
    ]),
    dbc.ModalBody([
        pop_graph := dcc.Graph(id="pop_graph_")
    ])
],
    id="pop_modal",
    scrollable=True,
    fullscreen=True,
)

STATISTICS = html.Div([
    html.Div([
        html.H4("Statistics", style={"display": "inline-block"}),
        html.Div(
            [
                html.Div(
                    [
                        # html.H4(
                        #     "Statistics",
                        #     style={
                        #         "display": "inline-block",
                        #         "textIndent": "100%",
                        #         "overflow": "hidden"
                        #     }
                        # ),
                        group_by_button := html.Button(
                            "Group by ...",
                            n_clicks=rc.statisticsGroupByType,
                            id="group_by_button_",
                            style={
                                "display": "inline-block",
                                "margin": "7px",
                                "fontSize": "13px",
                                "paddingLeft": "10px",
                                "paddingRight": "10px",
                            }
                        ),
                        group_by_trigger := html.Div(id="group_by_trigger_", n_clicks=rc.statisticsGroupByType, style={"display": "none"}),
                        settings_button := html.Button(
                            "Framing…",
                            id="settings_button_",
                            style={
                                      "display": "inline-block",
                                      "margin": "7px",
                                      "fontSize": "13px",
                                      "paddingLeft": "10px",
                                      "paddingRight": "10px",
                                  } | styles.misc.trailing_options
                        ),
                        html.Div(
                            html.Div(
                                performance_size_slider := dcc.Slider(
                                    **styles.figures.size_slider_kwargs_performance,
                                    id="performance_size_slider_",
                                    className="nopadding"
                                ),
                                style={
                                    "padding": "0px 10px",
                                    "paddingBottom": "5px",
                                    "width": 450
                                } | styles.misc.performance_size
                            ),
                            style={
                                "display": "inline-block"
                            }
                        )
                    ],
                    style={
                        "whiteSpace": "nowrap"
                    }
                )
            ],
            style={
                "overflow": "hidden",
                "position": "absolute",
                "zIndex": 1,
                "display": "inline-block"
            },
            className="fill-available-width"
        ),
    ]),
    html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(html.H6("Open Positions"), style={"width": "90%", "display": "inline-block"}),
                            pop_open_positions := html.Div("⇱", style={"width": "10%", "display": "inline-block", "fontSize": "18px", "textAlign": "end", "cursor": "pointer"}, id="pop_open_positions_", n_clicks=0),
                        ]
                    ),
                    open_positions_graph := dcc.Graph("open_positions_graph_", config={'displaylogo': False}),
                ],
                style={
                    "width": "100%",
                    "padding": "10px"
                }
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(html.H6("Positions of Alltime"), style={"width": "90%", "display": "inline-block"}),
                            pop_all_positions := html.Div("⇱", style={"width": "10%", "display": "inline-block", "fontSize": "18px", "textAlign": "end", "cursor": "pointer"}, id="pop_all_positions_", n_clicks=0),
                        ]
                    ),
                    all_positions_graph := dcc.Graph("all_positions_graph_", config={'displaylogo': False}),
                ],
                style={
                    "width": "100%",
                    "padding": "10px"
                }
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(html.H6("Performance"), style={"width": "90%", "display": "inline-block"}),
                            pop_performance := html.Div("⇱", style={"width": "10%", "display": "inline-block", "fontSize": "18px", "textAlign": "end", "cursor": "pointer"}, id="pop_performance_", n_clicks=0),
                        ],
                        style={"display": "flex"}
                    ),
                    html.Div([
                        drag_container := html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div("☰", style={"border": "1px solid", "width": "5240%", "height": "100%"})
                                    ],
                                    id="drag_component-%d" % i,
                                    style={
                                        "height": "calc(100% / 7)",
                                        "cursor": "row-resize",
                                        "fontSize": "18px",
                                        "borderRight": "1px solid",
                                        "width": "100%",
                                    }
                                )
                                for i in range(1, 8)
                            ],
                            id="drag_container_",
                            style={
                                "display": "inline-block",
                                "width": "2%",
                                "height": "%dpx" % styles.figures.size_slider_kwargs_performance["value"]
                            }
                        ),
                        html.Div(
                            performance_graph := dcc.Graph("performance_graph_", config={'displaylogo': False}),
                            style={
                                "display": "inline-block",
                                "width": "98%"
                            }
                        )
                    ],
                        style={"display": "flex"}
                    )
                ],
                style={
                    "width": "100%"
                }
            ),
        ]
    )
],
    id="statistics_",
    style={
        "height": "100%",
        "overflowY": "scroll",
        "overflowX": "hidden",
        "display": ("" if rc.sideInitStatisticValue else "none")
    }
)
