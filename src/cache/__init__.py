from __future__ import annotations

import pickle
from time import time
from datetime import datetime
from os import mkdir, listdir, remove
from urllib.parse import unquote
from re import finditer

import src
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
    t = int(time())
    try:
        print("[ INIT ]/journal load:", rc.CACHE_TRADINGLOG)
        with open(rc.CACHE_TRADINGLOG, "rb") as __f:
            INIT_DATA = pickle.load(__f)
    except FileNotFoundError:
        print("[ INIT ]/journal first run:", __firstrun)
        INIT_DATA = __firstrun
        dump_log(INIT_DATA)
    try:
        print("[ INIT ]/history load:", rc.CACHE_TRADINGLOG_HISTORY)
        with open(rc.CACHE_TRADINGLOG_HISTORY, "rb") as __f:
            HISTORY_DATA = pickle.load(__f)
    except FileNotFoundError:
        print("[ INIT ]/history first run:", __firstrun)
        HISTORY_DATA = {i: {"time": i, "data": __firstrun} for i in range(rc.nHistorySlots)}

    try:
        print("[ INIT ]/file-clones/flush load:", src.FILE_CLONES_FLUSH_TIMESTAMP)
        with open(src.FILE_CLONES_FLUSH_TIMESTAMP) as __f:
            timestamp = int(__f.read())
        if timestamp + rc.noteFileDropClonerFlushIntervalS < t:
            print("[ INIT ]/file-clones/flush start")
            with open(src.FILE_CLONES_FLUSH_TIMESTAMP, "w") as __f:
                __f.write(str(t))

            if fileclones := listdir(src.FILE_CLONES):

                for row in INIT_DATA:
                    if note := row.get("Note"):
                        for m in finditer("(\\[[^\\]*]\\])(\\([^\\)]+\\))", note):
                            link = unquote(m.group(2))
                            try:
                                fileclones.remove(link)
                            except ValueError:
                                if not fileclones:
                                    break

                print("[ INIT ]/file-clones/flush trash:", src.FILE_CLONES_TRASH)
                for trash in listdir(src.FILE_CLONES_TRASH):
                    remove(f"{src.FILE_CLONES_TRASH}/{trash}")

                print("[ INIT ]/file-clones/flush unused files:", fileclones)
                if rc.noteFileDropClonerFlushTrashing:
                    for fileclone in fileclones:
                        with open(path := f"{src.FILE_CLONES}/{fileclone}", "rb") as _if:
                            with open(f"{src.FILE_CLONES_TRASH}/{fileclone}", "wb") as _of:
                                _of.write(_if.read())
                        remove(path)
                else:
                    for fileclone in fileclones:
                        remove(f"{src.FILE_CLONES}/{fileclone}")

    except FileNotFoundError:
        print("[ INIT ]/file-clones first run")
        with open(src.FILE_CLONES_FLUSH_TIMESTAMP, "w") as __f:
            __f.write(str(t))
        try:
            mkdir(src.FILE_CLONES)
        except FileExistsError:
            pass
        try:
            mkdir(src.FILE_CLONES_TRASH)
        except FileExistsError:
            pass

        INIT_DATA = __firstrun
        dump_log(INIT_DATA)

    print("[ INIT ]/plugin call")
    do_dump = plugin.init_log(INIT_DATA)
    make_hist = plugin.init_history(HISTORY_DATA)

    HISTORY_KEYS_X_TIME_REVSORT = list((k, v["time"]) for k, v in HISTORY_DATA.items())
    HISTORY_KEYS_X_TIME_REVSORT.sort(key=lambda x: x[1], reverse=True)

    def make_history():
        global LAST_HISTORY_CREATION_TIME
        LAST_HISTORY_CREATION_TIME = t
        HISTORY_DATA[HISTORY_KEYS_X_TIME_REVSORT[-1][0]] = {"time": LAST_HISTORY_CREATION_TIME, "data": INIT_DATA}
        with open(rc.CACHE_TRADINGLOG_HISTORY, "wb") as __f:
            pickle.dump(HISTORY_DATA, __f, PICKLE_PROTOCOL)

    if do_dump:
        print("[ INIT ]/plugin/journal -> dump")
        dump_log(INIT_DATA)
        make_history()
    elif make_hist:
        print("[ INIT ]/plugin/history -> dump")
        with open(rc.CACHE_TRADINGLOG_HISTORY, "wb") as __f:
            pickle.dump(HISTORY_DATA, __f, PICKLE_PROTOCOL)
    else:
        newest_backup = HISTORY_DATA[HISTORY_KEYS_X_TIME_REVSORT[0][0]]["data"]

        if len(INIT_DATA) != len(newest_backup):
            print("[ INIT ]/history/n-entries -> create+dump")
            make_history()
            return

        initdata = INIT_DATA.copy()
        initdata.sort(key=lambda x: x["id"])
        newest_backup.sort(key=lambda x: x["id"])
        comp_keys = ("id", "Name", "n", "InvestTime", "InvestAmount", "TakeTime", "TakeAmount", "ITC", "Note")

        for ini, bku in zip(initdata, newest_backup):
            if tuple(ini.get(k) for k in comp_keys) != tuple(bku.get(k) for k in comp_keys):
                print("[ INIT ]/history/cell-contents -> create+dump")
                make_history()
                return

        print("[ INIT ]/history no changes")

    LAST_HISTORY_CREATION_TIME = HISTORY_DATA[HISTORY_KEYS_X_TIME_REVSORT[0][0]]["time"]


def dump_log(data: list[dict]):
    with open(rc.CACHE_TRADINGLOG, "wb") as __f:
        pickle.dump(data, __f, PICKLE_PROTOCOL)
