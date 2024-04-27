from src.config import color_theme, rc

by_taketime_on = {"color": color_theme.table_fg_header, "border": "1px solid " + color_theme.table_sep, "backgroundColor": color_theme.col_take, "backgroundImage": ""}
by_taketime_off = by_taketime_on | {"backgroundColor": color_theme.col_invest}

by_index_off = by_taketime_on | {"backgroundColor": color_theme.table_bg_main, "backgroundImage": color_theme.top_by_index_off}

with_open_on = {"color": color_theme.table_fg_main, "border": "1px solid " + color_theme.table_sep, "backgroundColor": color_theme.record_opentrade}
with_open_off = by_taketime_on | {"color": color_theme.table_fg_header, "backgroundColor": color_theme.table_bg_main}

autosave_on = {"color": color_theme.top_onoff_fg, "border": "1px solid " + color_theme.table_sep, "backgroundColor": color_theme.top_onoff_bg}
autosave_off = {"color": color_theme.table_fg_header, "border": "1px solid " + color_theme.table_sep, "backgroundColor": ""}

by_type_on = {"color": color_theme.table_fg_main, "border": "1px solid " + color_theme.table_sep, "backgroundColor": color_theme.col_type or color_theme.table_bg_main}
by_type_off = by_type_on | {"color": color_theme.table_fg_header, "backgroundColor": (color_theme.col_symbol if rc.statisticsIdBySymbol else color_theme.col_name) or color_theme.table_bg_main}

trailing_options = {"color": color_theme.table_fg_main, "border": "1px solid " + color_theme.table_sep, "backgroundColor": color_theme.table_bg_main}
performance_size = {}

interval_on = {"color": color_theme.top_onoff_fg, "border": "1px solid " + color_theme.table_sep, "backgroundColor": color_theme.top_onoff_bg}
interval_off = {"color": color_theme.table_fg_header, "border": "1px solid " + color_theme.table_sep, "backgroundColor": ""}

summary_footer = {"color": color_theme.table_fg_main, "backgroundColor": color_theme.table_bg_header}
summary_error = {"borderTop": "5px solid " + color_theme.mark_error}
summary_error_reset = {"borderTop": ""}

statistics_button = {
    "color": color_theme.table_fg_main,
    "backgroundColor": color_theme.table_bg_main,
    "border": "1px solid " + color_theme.statistics_button_border,
    "boxShadow": color_theme.statistics_button_shadow + " 0px 3px 10px",
}
balance_button = {
    "color": color_theme.table_fg_main,
    "backgroundColor": color_theme.table_bg_main,
    "border": "1px solid " + color_theme.balance_button_border,
    "boxShadow": color_theme.balance_button_shadow + " 0px 3px 10px",
}
statistics_split_handle = {
    "backgroundColor": color_theme.statistics_button_border,
    "border": "1px solid " + color_theme.statistics_button_border,
    "boxShadow": color_theme.statistics_button_shadow + " 0px 3px 10px",
    "width": "2px",
}
balance_split_handle = {
    "backgroundColor": color_theme.balance_button_border,
    "border": "1px solid " + color_theme.balance_button_border,
    "boxShadow": color_theme.balance_button_shadow + " 0px 3px 10px",
}

header = {"borderBottom": "1px solid " + color_theme.table_sep}
