from re import sub
from sys import argv

import plugin
import src.config.rc as rc
import src

from pathlib import Path

from . import make

ID = ""
ROOT = sub("[^/\\\\]+$", "", __file__)
CACHE_ROOT = ROOT + "/"
_CACHE_TRADINGLOG = CACHE_ROOT + "/demo-%s-tradinglog.pkl"
_CACHE_TRADINGLOG_HISTORY = CACHE_ROOT + "/demo-%s-tradinglog-history.pkl"
CACHE_TRADINGLOG = _CACHE_TRADINGLOG
CACHE_TRADINGLOG_HISTORY = _CACHE_TRADINGLOG_HISTORY

DEMO_BU = CACHE_ROOT + "/~demo--tradinglog.pickle"


def init(id_: str):
    global ID, CACHE_TRADINGLOG, CACHE_TRADINGLOG_HISTORY

    ID = id_
    CACHE_TRADINGLOG = _CACHE_TRADINGLOG % ID
    CACHE_TRADINGLOG_HISTORY = _CACHE_TRADINGLOG_HISTORY % ID

    src.CACHE_ROOT = CACHE_ROOT
    src.CACHE_TRADINGLOG = CACHE_TRADINGLOG
    src.CACHE_TRADINGLOG_HISTORY = CACHE_TRADINGLOG_HISTORY

    if not Path(CACHE_TRADINGLOG).exists():
        with open(DEMO_BU, "rb") as _if:
            with open(CACHE_TRADINGLOG, "wb") as _of:
                _of.write(_if.read())


_make = False
_make_and_run = False
_plugin = False

for arg in argv[1:]:
    if arg.startswith("make="):
        ID = arg[5:]
        _make = True
    elif arg.startswith("make"):
        init(ID)
        _make = True
    elif arg == "run":
        _make_and_run = True
    elif arg == "plugin":
        _plugin = True
    else:
        ID = arg


if _make:
    init(ID)
    make.make()
    print(f"demo({ID=}) created")
    if not _make_and_run:
        exit()
if _plugin:

    rc.coursePluginUpdateInterval = 1
    rc.cellRendererChangeTakeCourse = 1

    def course_call(row_data: dict, manual_take_amount: bool) -> bool:
        if not manual_take_amount:
            c = row_data.get("TakeCourse") or row_data["InvestCourse"]
            if c:
                if make.randint(0, 1):
                    c *= (1 + make.randrate2())
                else:
                    c *= (1 - make.randrate2())
                row_data["TakeCourse"] = c
                row_data["TakeAmount"] = row_data["n"]
                return True
        else:
            return False


    plugin.course_call = course_call

    def symbol_call(update_data: dict) -> None:
        if asset := make.example_assets.get(update_data.get("value")):
            update_data["data"] |= {"Symbol": asset[2], "Type": asset[1]}

    plugin.symbol_call = symbol_call

rc.logColWidths[1] = 70
rc.logColWidths[2] = 70
rc.statisticsGroupByType = 1
rc.noteMathJax = 1
