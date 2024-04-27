from datetime import datetime

from src.config import time_formats


def make_history_list(history: list[tuple[int, int]]):
    return [
        {"value": v, "label": datetime.fromtimestamp(l).strftime(time_formats.history_time_format)}
        for v, l in history
    ]
