from datetime import timedelta
from src.config import rc

# eval(option["value"])

_rc = {
    "w": repr(timedelta(weeks=1)),
    "m": repr(timedelta(weeks=4)),
    "q": repr(timedelta(weeks=13)),
    0: repr(timedelta(0)),
    12: repr(timedelta(weeks=52)),
    24: repr(timedelta(weeks=104)),
    48: repr(timedelta(weeks=208)),
}

performance_steps = [
    {"label": "Week Frames", "value": repr(timedelta(weeks=1))},
    {"label": "Month Frames", "value": repr(timedelta(weeks=4))},
    {"label": "Quarter Frames", "value": repr(timedelta(weeks=13))},
]
performance_steps_default = _rc[rc.statisticsPerformanceStepsDefault]

performance_interval = [
    {"label": "~Trailing : Week Interval", "value": repr(timedelta(weeks=1))},
    {"label": "~Trailing : Month Interval", "value": repr(timedelta(weeks=4))},
    {"label": "~Trailing : Quarter Interval", "value": repr(timedelta(weeks=13))},
]
performance_interval_default = _rc[rc.statisticsPerformanceIntervalDefault]

performance_frame = [
    {"label": "~Trailing : Week Frame", "value": repr(timedelta(weeks=1))},
    {"label": "~Trailing : Month Frame", "value": repr(timedelta(weeks=4))},
    {"label": "~Trailing : Quarter Frame", "value": repr(timedelta(weeks=13))},
]
performance_frame_default = _rc[rc.statisticsPerformanceFrameDefault]

performance_range = [
    {"label": "All Scope", "value": repr(timedelta(0))},
    {"label": "12 Months", "value": repr(timedelta(weeks=52))},
    {"label": "24 Months", "value": repr(timedelta(weeks=104))},
    {"label": "48 Months", "value": repr(timedelta(weeks=208))},
]
performance_range_default = _rc[rc.statisticsPerformanceRangeDefault]
