from re import sub
from sys import argv

try:
    _make = False
    _make_and_run = False
    _plugin = False
    _years = 3
    ID = ""
except Exception:
    raise

try:

    arg0 = argv[1]
    if len(argv) == 2:
        ID = argv.pop(1)
    elif arg0 == "-":
        argv.pop(1)
        ID = argv.pop(1)
    elif arg0.startswith("make="):
        ID = argv.pop(1)[5:]
        _make = True
        if "#" in ID:
            _years = int(ID.split("#")[0])
    elif arg0.startswith("make"):
        _make = True
        argv.pop(1)
        if "#" in arg0:
            _years = int(arg0.split("#")[0])
    try:
        argv.remove("run")
        _make_and_run = True
    except ValueError:
        pass
    try:
        argv.remove("plugin")
        _plugin = True
    except ValueError:
        pass
except IndexError:
    pass

import plugin
import rconfig

from pathlib import Path

ROOT = sub("[^/\\\\]+$", "", __file__)
CACHE_ROOT = ROOT + "/"
_CACHE_TRADINGLOG = "/demo-%s-tradinglog.pkl"
_CACHE_TRADINGLOG_HISTORY = "/demo-%s-tradinglog-history.pkl"
CACHE_TRADINGLOG = CACHE_ROOT + _CACHE_TRADINGLOG
CACHE_TRADINGLOG_HISTORY = CACHE_ROOT + _CACHE_TRADINGLOG_HISTORY

DEMO_BU = CACHE_ROOT + "/~demo--tradinglog.pickle"


def init(id_: str):
    global ID, CACHE_TRADINGLOG, CACHE_TRADINGLOG_HISTORY

    from src.config import rc
    from . import make

    ID = id_
    CACHE_TRADINGLOG = CACHE_ROOT + (_CACHE_TRADINGLOG % ID)
    CACHE_TRADINGLOG_HISTORY = CACHE_ROOT + (_CACHE_TRADINGLOG_HISTORY % ID)

    rc.CACHE_TRADINGLOG = CACHE_TRADINGLOG
    rc.CACHE_TRADINGLOG_HISTORY = CACHE_TRADINGLOG_HISTORY

    if not Path(CACHE_TRADINGLOG).exists():
        with open(DEMO_BU, "rb") as _if:
            with open(CACHE_TRADINGLOG, "wb") as _of:
                _of.write(_if.read())

    if _make:
        make.make(_years)
        print(f"demo({ID=}) created")
        if not _make_and_run:
            exit()


if _plugin:

    rconfig.coursePluginUpdateInterval = 1
    rconfig.coursePluginUpdateIntervalOn = 1
    rconfig.cellRendererChangeTakeCourse = 1

    def course_call(row_data: dict, manual_take_amount: bool) -> bool:
        from . import make
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
        from . import make
        if asset := make.example_assets.get(update_data.get("value")):
            update_data["data"] |= {"Symbol": asset[2], "Type": asset[1]}

    plugin.symbol_call = symbol_call

rconfig.logColWidths[1] = 70
rconfig.logColWidths[2] = 70
rconfig.statisticsGroupByType = 1
rconfig.noteMathJax = 1
