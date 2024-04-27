import pickle

from rconfig import *
from src import ROOT, CACHE_COLORS
from src.config import color_theme
from src.config.styles.figures import color_palette_donut


with open(ROOT + "/assets/rc.js", "w") as f:
    f.write(
        "// [do not change] this file is created by `rc'\n"
        f"const {gridDefWidthScale=};"
        f"const {gridMinWidthScale=};"
        f"const {gridRow3Height=};"
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

_colorPalette = color_palette_donut.copy()


def get_position_color(__key):
    global _colorPalette
    try:
        return _colorCache[__key]
    except KeyError:
        try:
            color = _colorPalette.pop(0)
        except IndexError:
            _colorPalette = color_palette_donut.copy()
            color = _colorPalette.pop(0)
        _colorCache[__key] = color
        _dump_color_cache()
        return color
