from __future__ import annotations

import pickle
from time import time
from datetime import datetime

from src import CACHE_TRADINGLOG, CACHE_TRADINGLOG_HISTORY
from src.config import rc
import plugin


INIT_DATA: list[dict]
HISTORY_DATA: dict
HISTORY_KEYS_X_TIME_REVSORT: list[tuple[int, int]]
LAST_HISTORY_CREATION_TIME: int

PICKLE_PROTOCOL = pickle.HIGHEST_PROTOCOL


def init():
    global INIT_DATA, HISTORY_DATA, HISTORY_KEYS_X_TIME_REVSORT, LAST_HISTORY_CREATION_TIME
    __firstrun = [{"id": 0, "n": 0, "InvestTime": datetime.now().strftime(rc.timeFormatTransaction), "InvestAmount": 1}]
    try:
        with open(CACHE_TRADINGLOG, "rb") as __f:
            INIT_DATA = pickle.load(__f)
    except FileNotFoundError:
        INIT_DATA = __firstrun
        dump_log(INIT_DATA)
    try:
        with open(CACHE_TRADINGLOG_HISTORY, "rb") as __f:
            HISTORY_DATA = pickle.load(__f)
    except FileNotFoundError:
        HISTORY_DATA = {i: {"time": i, "data": __firstrun} for i in range(rc.nHistorySlots)}

    do_dump = plugin.init_log(INIT_DATA)
    make_hist = plugin.init_history(HISTORY_DATA)

    HISTORY_KEYS_X_TIME_REVSORT = list((k, v["time"]) for k, v in HISTORY_DATA.items())
    HISTORY_KEYS_X_TIME_REVSORT.sort(key=lambda x: x[1], reverse=True)

    def make_history():
        global LAST_HISTORY_CREATION_TIME
        LAST_HISTORY_CREATION_TIME = int(time())
        HISTORY_DATA[HISTORY_KEYS_X_TIME_REVSORT[-1][0]] = {"time": LAST_HISTORY_CREATION_TIME, "data": INIT_DATA}
        with open(CACHE_TRADINGLOG_HISTORY, "wb") as __f:
            pickle.dump(HISTORY_DATA, __f, PICKLE_PROTOCOL)

    if do_dump:
        dump_log(INIT_DATA)
        make_history()
        print(f"[HISTORY]++ (init -> do_dump)")
    elif make_hist:
        make_history()
        print(f"[HISTORY]++ (init -> make_hist)")
    else:
        newest_backup = HISTORY_DATA[HISTORY_KEYS_X_TIME_REVSORT[0][0]]["data"]

        if len(INIT_DATA) != len(newest_backup):
            make_history()
            print(f"[HISTORY]++ (n records)")
            return

        initdata = INIT_DATA.copy()
        initdata.sort(key=lambda x: x["id"])
        newest_backup.sort(key=lambda x: x["id"])
        comp_keys = ("id", "Name", "n", "InvestTime", "InvestAmount", "TakeTime", "TakeAmount", "ITC", "Note")

        for ini, bku in zip(initdata, newest_backup):
            if tuple(ini.get(k) for k in comp_keys) != tuple(bku.get(k) for k in comp_keys):
                make_history()
                print(f"[HISTORY]++ (cells changed)")
                return

        print(f"[HISTORY]|| (no changes)")

    LAST_HISTORY_CREATION_TIME = HISTORY_DATA[HISTORY_KEYS_X_TIME_REVSORT[0][0]]["time"]


def dump_log(data: list[dict]):
    with open(CACHE_TRADINGLOG, "wb") as __f:
        pickle.dump(data, __f, PICKLE_PROTOCOL)
