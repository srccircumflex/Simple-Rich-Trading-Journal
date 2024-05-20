import pickle
from ast import literal_eval

from rconfig import *
try:
    from prconfig import *
except ImportError:
    pass

from . import color_theme
from src import ROOT, CACHE_ROOT, CACHE_COLORS, template_CACHE_TRADINGLOG, template_CACHE_TRADINGLOG_HISTORY

import rconfig
from sys import argv as _argv
_argv = _argv[1:]

profile_name = ""
CACHE_TRADINGLOG = CACHE_ROOT + (template_CACHE_TRADINGLOG % profile_name)
CACHE_TRADINGLOG_HISTORY = CACHE_ROOT + (template_CACHE_TRADINGLOG_HISTORY % profile_name)

if len(_argv) == 1:
    profile_name = _argv[0]
    _arg = "-" + profile_name
    CACHE_TRADINGLOG = CACHE_ROOT + (template_CACHE_TRADINGLOG % _arg)
    CACHE_TRADINGLOG_HISTORY = CACHE_ROOT + (template_CACHE_TRADINGLOG_HISTORY % _arg)
else:
    _globals = globals()
    while _argv:
        _config_key = _argv.pop(0)
        if _config_key == "-":
            profile_name = _argv.pop(0)
            _arg = "-" + profile_name
            CACHE_TRADINGLOG = CACHE_ROOT + (template_CACHE_TRADINGLOG % _arg)
            CACHE_TRADINGLOG_HISTORY = CACHE_ROOT + (template_CACHE_TRADINGLOG_HISTORY % _arg)
        elif _config_key.endswith("]"):
            _config_key, _idx = _config_key[:-1].split("[")
            _attr = getattr(rconfig, _config_key)
            _attr.__setitem__(int(_idx), type(_attr[0])(_argv.pop(0)))
        elif (_attrt := type(_attr := getattr(rconfig, _config_key))) is list:
            _arg = _argv.pop(0)
            if not _arg.startswith("["):
                raise ValueError(f"{_config_key!r} requires a value of type <list> whose pattern corresponds to [1, 2, ...]. {_arg!r} is received.")
            while not _arg.endswith("]"):
                _arg += _argv.pop(0)
            _globals[_config_key] = literal_eval(_arg)
        else:
            _globals[_config_key] = _attrt(_argv.pop(0))


color_theme._load_theme(colorTheme)


dateFormat = {"ISO 8601": "ydm", "american": "mdy", "international": "dmy"}.get(dateFormat, dateFormat)
timeFormatTransaction, timeFormatHistory, timeFormatDaterange, timeFormatLastCalc = {
    "ydm": ("%y/%d/%m %H:%M", "\u2007\u2007%a. %y/%d/%m %H:%M.%S", "YY/DD/MM", "%y / %d / %m"),
    "mdy": ("%m/%d/%y %H:%M", "\u2007\u2007%a. %m/%d/%y %H:%M.%S", "MM/DD/YY", "%m / %d / %y"),
    "dmy": ("%d/%m/%y %H:%M", "\u2007\u2007%a. %d/%m/%y %H:%M.%S", "DD/MM/YY", "%d / %m / %y"),
}[dateFormat]


with open(ROOT + "/assets/rc.js", "w") as f:
    f.write(
        "// [do not change] this file is created by `rc'\n"
        f"const {gridDefWidthScale=};"
        f"const {gridMinWidthScale=};"
        f"const {gridRow3Height=};"
        f"const {dateFormat=};"
        f"const ccCopy = {bindKeyCodes[0]!r};"
        f"const ccCut = {bindKeyCodes[1]!r};"
        f"const ccPaste = {bindKeyCodes[2]!r};"
        f"const ccCopyRow1 = {bindKeyCodes[3]!r};"
        f"const ccCopyRow2 = {bindKeyCodes[4]!r};"
        f"const ccCopyRow3 = {bindKeyCodes[5]!r};"
        f"const ccAComplete = {bindKeyCodes[6]!r};"
        f"const ccNote = {bindKeyCodes[7]!r};"
        f"const ccNoteBack = {bindKeyCodes[8]!r};"
        f"const {noteCellVariableFormatter=};"
        f"const {noteUnifying=};"
        f"const noteLinkDropPattern=/{noteLinkDropPattern}/;"
        f"const notePathDropPattern=/{notePathDropPattern}/;"
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
    cont += """
/* notepaper > */
.notepaper a {
  color: %s !important;
}
/* < notepaper */
""" % color_theme.notepaper_link
    cont += """
/* note editor > */
.CodeMirror {
  height: 100%%;
  width: 100%%;
  background-color: %s;
}
.CodeMirror-gutters {
  background-color: %s;
}
/* < note editor */
""" % (
        color_theme.notebook_bg + (color_theme.notebook_def_transparency if noteEditorDefaultTransparency else ""),
        color_theme.notebook_gutter_bg + (color_theme.notebook_def_gutter_transparency if noteEditorDefaultTransparency else ""),
    )

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

_idx = 0


def get_footer_live_signal():
    global _idx
    _idx += 1
    if _idx % 2:
        return {"borderTop": "1px solid " + color_theme.footer_sig2}
    else:
        return {"borderTop": "1px solid " + color_theme.footer_sig1}


_d = dict()

if disableFooterLifeSignal:
    def get_footer_live_signal():
        return _d
