from dash import html, dcc

from src.config import styles, rc, time_formats

_Deposits = "\u2007Deposits \u2007\u2007"
_Payouts = "\u2007Payouts \u2007\u2007"
_Fin = "\u2007Fin Trades \u2007\u2007"
_Open = "\u2007Open Trades \u2007\u2007"
_Dividends = "\u2007Dividends \u2007\u2007"
_ITCs = "\u2007ITCs \u2007\u2007"
_Undefined = "\u2007Undefined \u2007\u2007"

scopes_x_func = {
    _Deposits: "params.data.cat == 'd'",
    _Payouts: "params.data.cat == 'p'",
    _Fin: "params.data.cat == 'tf'",
    _Open: "params.data.cat == 'to'",
    _Dividends: "(params.data.cat == 'v') || (params.data.cat == 'tf' && params.data.Dividend) || (params.data.cat == 'to' && params.data.Dividend)",
    _ITCs: "params.data.cat == 'i'",
    _Undefined: "params.data.cat == ''"
}

_layout = [
    {"value": _Deposits, "label": html.Span(_Deposits, style=styles.log.name_DEPOSIT_tag)},
    {"value": _Payouts, "label": html.Span(_Payouts, style=styles.log.name_PAYOUT_tag)},
    {"value": _Fin, "label": html.Span(_Fin, style={"color": styles.color_theme.table_fg_main})},
    {"value": _Open, "label": html.Span(_Open, style=styles.log.name_opentrade)},
    {"value": _Dividends, "label": html.Span(_Dividends, style=styles.log.name_dividend)},
    {"value": _ITCs, "label": html.Span(_ITCs, style=styles.log.name_ITC_tag)},
    {"value": _Undefined, "label": html.Span(_Undefined, style=styles.log.name_undefined)},
]

scopes_check = dcc.Checklist(
    options=_layout,
    value=list(),
    inline=True,
    id="scopes_",
    style={
        "fontSize": "13px",
        "padding": "10px",
        "display": "inline-block",
    },
    className="noselect"
)
search_input = dcc.Input(
    placeholder="Search ...",
    id="search_input_",
    style={
        "margin": "7px",
        "fontSize": "13px",
        "display": "inline-block",
    }
)
auto_save_button = html.Button(
    "Auto. Save",
    n_clicks=1,
    id="auto_save_button_",
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
    }
)
reload_button = html.Button(
    "Reload",
    id="reload_button_",
    n_clicks=0,
    style={
        # todo "display": "inline-block",
        "display": "none",

        "margin": "7px",
        "fontSize": "13px",
        "color": styles.color_theme.table_fg_header,
        "backgroundColor": styles.color_theme.table_bg_main,
        "border": "1px solid " + styles.color_theme.table_sep,
        "paddingLeft": "10px",
        "paddingRight": "10px",
    }
)
history_button = html.Button(
    "History",
    id="history_button_",
    n_clicks=0,
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "color": styles.color_theme.table_fg_header,
        "backgroundColor": styles.color_theme.table_bg_main,
        "border": "1px solid " + styles.color_theme.table_sep,
        "paddingLeft": "10px",
        "paddingRight": "10px",
    }
)
export_button = html.Button(
    "Export",
    id="export_button_",
    n_clicks=0,
    style={
        # todo "display": "inline-block",
        "display": "none",

        "margin": "7px",
        "fontSize": "13px",
        "color": styles.color_theme.table_fg_header,
        "backgroundColor": styles.color_theme.table_bg_main,
        "border": "1px solid " + styles.color_theme.table_sep,
        "paddingLeft": "10px",
        "paddingRight": "10px",
    }
)
import_button = html.Button(
    "Import",
    id="import_button_",
    n_clicks=0,
    style={
        # todo "display": "inline-block",
        "display": "none",

        "margin": "7px",
        "fontSize": "13px",
        "color": styles.color_theme.table_fg_header,
        "backgroundColor": styles.color_theme.table_bg_main,
        "border": "1px solid " + styles.color_theme.table_sep,
        "paddingLeft": "10px",
        "paddingRight": "10px",
    }
)
statistics_button = html.Button(
    "STATISTICS",
    id="statistics_button_",
    n_clicks=rc.sideInitStatisticValue,
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "paddingLeft": "10px",
        "paddingRight": "10px",
    } | styles.misc.statistics_button
)
balance_button = html.Button(
    "BALANCE",
    id="balance_button_",
    n_clicks=rc.sideInitBalanceValue,
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "paddingLeft": "10px",
        "paddingRight": "10px",
    } | styles.misc.balance_button
)
daterange = dcc.DatePickerRange(
    clearable=True,
    display_format=time_formats.daterange_time_format,
    start_date_placeholder_text=time_formats.daterange_time_format,
    end_date_placeholder_text=time_formats.daterange_time_format,
    first_day_of_week=time_formats.first_day_of_week,
    number_of_months_shown=6,
    day_size=20,
    id="daterange_",
    style={
        "margin": "7px",
        "fontSize": "13px",
    }
)
index_by_button = html.Button(
    "Index by ...",
    n_clicks=rc.indexByTakeTime,
    id="index_by_button_",
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "paddingLeft": "10px",
        "paddingRight": "10px",
    }
)
scope_by_button = html.Button(
    "Scope by ...",
    n_clicks=rc.scopeByIndex,
    id="scope_by_button_",
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "paddingLeft": "10px",
        "paddingRight": "10px",
    }
)
with_open_button = html.Button(
    "with open",
    n_clicks=rc.calcWithOpens,
    id="with_open_button_",
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "paddingLeft": "10px",
        "paddingRight": "10px",
    }
)
with_open_trigger = html.Div(id="with_open_trigger_", n_clicks=rc.calcWithOpens, style={"display": "none"})
_interval_n = rc.coursePluginUpdateInterval and rc.coursePluginUpdateIntervalOn
update_interval_button = html.Button(
    "⥁",
    n_clicks=_interval_n,
    id="update_interval_button_",
    style={
        "display": "inline-block",
        "margin": "7px",
        "fontSize": "13px",
        "paddingLeft": "10px",
        "paddingRight": "10px",
    },
    disabled=not rc.coursePluginUpdateInterval
)
update_interval_button_trigger = html.Div(id="update_interval_button_trigger_", n_clicks=_interval_n, style={"display": "none"})
update_interval = dcc.Interval(id="update_interval_", interval=rc.coursePluginUpdateIntervalMs, disabled=(not rc.coursePluginUpdateInterval) or (not rc.coursePluginUpdateIntervalOn))
update_interval_trigger = html.Div(id="update_interval_trigger_", n_clicks=_interval_n, style={"display": "none"})
