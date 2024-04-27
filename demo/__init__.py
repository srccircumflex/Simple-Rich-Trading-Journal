from re import sub
from sys import argv

import plugin
from src.config import rc
import src

from . import make

ID = ""
ROOT = sub("[^/\\\\]+$", "", __file__)
CACHE_ROOT = ROOT + "/"
_CACHE_TRADINGLOG = CACHE_ROOT + "/demo-%s-tradinglog.pickle"
_CACHE_TRADINGLOG_HISTORY = CACHE_ROOT + "/demo-%s-tradinglog-history.pickle"
CACHE_TRADINGLOG = _CACHE_TRADINGLOG
CACHE_TRADINGLOG_HISTORY = _CACHE_TRADINGLOG_HISTORY


def init(id_: str):
    global ID, CACHE_TRADINGLOG, CACHE_TRADINGLOG_HISTORY

    ID = id_
    CACHE_TRADINGLOG = _CACHE_TRADINGLOG % ID
    CACHE_TRADINGLOG_HISTORY = _CACHE_TRADINGLOG_HISTORY % ID

    src.CACHE_ROOT = CACHE_ROOT
    src.CACHE_TRADINGLOG = CACHE_TRADINGLOG
    src.CACHE_TRADINGLOG_HISTORY = CACHE_TRADINGLOG_HISTORY


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

    def course_call(row_data: dict) -> bool:
        c = row_data["InvestCourse"]
        if make.randint(0, 1):
            c *= (1 + make.randrate2())
        else:
            c *= (1 - make.randrate2())
        row_data["TakeCourse"] = c
        row_data["TakeAmount"] = row_data["n"]
        return True


    plugin.course_call = course_call

    def symbol_call(update_data: dict) -> None:
        if asset := make.example_assets.get(update_data["value"]):
            update_data["data"] |= {"Symbol": asset[2], "Type": asset[1]}

    plugin.symbol_call = symbol_call

rc.logColWidths[1] = 70
rc.logColWidths[2] = 70
rc.statisticsGroupByType = 1
