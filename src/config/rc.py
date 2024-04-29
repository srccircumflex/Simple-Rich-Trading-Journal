import pickle

from rconfig import *
try:
    from prconfig import *
except ImportError:
    pass

from .. import ROOT, CACHE_COLORS
from . import color_theme


dateFormat = {"ISO 8601": "ydm", "american": "mdy", "international": "dmy"}.get(dateFormat, dateFormat)
transactionTimeFormat = {"ydm": "%y/%d/%m %H:%M", "mdy": "%m/%d/%y %H:%M", "dmy": "%d/%m/%y %H:%M"}[dateFormat]

with open(ROOT + "/assets/rc.js", "w") as f:
    f.write(
        "// [do not change] this file is created by `rc'\n"
        f"const {gridDefWidthScale=};"
        f"const {gridMinWidthScale=};"
        f"const {gridRow3Height=};"
        f"const {dateFormat=};"
        f"const {transactionTimeFormat=};"
    )

with open(ROOT + "/assets/rc.css", "w") as f:
    cont = "/* [do not change] this file is created by `rc' */\n"
    cont += """
/* agGrid Input color > */
.%s input[class^=ag-] {
  color: %s !important;
}
/* < agGrid Input color */
""" % (color_theme.table_theme, color_theme.table_fg_main)
    if useDefaultAltColors:
        cont += """
/* agGrid alt colors > */
.ag-alt-colors {
    --ag-value-change-delta-down-color: %s !important;
    --ag-value-change-delta-up-color: %s !important;
}
/* < agGrid alt colors */
""" % (color_theme.alt_neg, color_theme.alt_pos)
    cont += """
/* dataTable hover bg > */
.dt-table-container__row-1 .cell-table tbody tr:hover td {
  background-color: %s !important;
}
/* < dataTable hover bg */
""" % color_theme.sheet_hover_bg
    f.write(cont)

if statisticsIdBySymbol:
    statisticsGroupId = "symbol"
else:
    statisticsGroupId = "name"

if gridSideSizeInitScale:
    gridSideSizeInitValue = int(gridSideSizeInitScale * 100)
    c2Width = f"{gridSideSizeInitValue}%"
    c1Width = f"{100 - gridSideSizeInitValue}%"
    sideInitBalanceValue = sideInitBalance
    sideInitStatisticValue = int(not sideInitBalance)
else:
    gridSideSizeInitValue = 0
    c2Width = "0%"
    c1Width = "100%"
    sideInitBalanceValue = 0
    sideInitStatisticValue = 0

_colorCache = dict()
if statisticsUsePositionColorCache:
    def _dump_color_cache():
        with open(CACHE_COLORS, "wb") as __f:
            pickle.dump(_colorCache, __f)


    try:
        with open(CACHE_COLORS, "rb") as __f:
            _colorCache = pickle.load(__f)
    except FileNotFoundError:
        _dump_color_cache()
else:
    def _dump_color_cache():
        pass

_colorPalette = color_theme.color_palette_donut.copy()


def get_position_color(__key):
    global _colorPalette
    try:
        return _colorCache[__key]
    except KeyError:
        try:
            color = _colorPalette.pop(0)
        except IndexError:
            _colorPalette = color_theme.color_palette_donut.copy()
            color = _colorPalette.pop(0)
        _colorCache[__key] = color
        _dump_color_cache()
        return color


cellRendererChangeTakeAmount = ({"cellRenderer": "agAnimateShowChangeCellRenderer"} if cellRendererChangeTakeAmount else {})
cellRendererChangeTakeCourse = ({"cellRenderer": "agAnimateShowChangeCellRenderer"} if cellRendererChangeTakeCourse else {})
cellRendererChangePerformance = ({"cellRenderer": "agAnimateShowChangeCellRenderer"} if cellRendererChangePerformance else {})
cellRendererChangeProfit = ({"cellRenderer": "agAnimateShowChangeCellRenderer"} if cellRendererChangeProfit else {})

nStatisticsDrag = len(set(statisticsPerformanceOrder))


if useDefaultAltColors:
    color_theme.cell_negvalue = color_theme.alt_neg
    color_theme.cell_posvalue = color_theme.alt_pos

_i = 0


def get_footer_live_signal():
    global _i
    _i += 1
    if _i % 2:
        return {"borderTop": "1px solid " + color_theme.footer_sig2}
    else:
        return {"borderTop": "1px solid " + color_theme.footer_sig1}


_d = dict()

if disableFooterLifeSignal:
    def get_footer_live_signal():
        return _d
