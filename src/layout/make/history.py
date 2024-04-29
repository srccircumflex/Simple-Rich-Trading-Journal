from datetime import datetime

from src.config import rc


def make_history_list(history: list[tuple[int, int]]):
    return [
        {"value": v, "label": datetime.fromtimestamp(l).strftime(rc.timeFormatHistory)}
        for v, l in history
    ]
