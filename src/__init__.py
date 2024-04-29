from . import *
from re import sub

ROOT = sub("[^/\\\\]+$", "", __file__)

CACHE_ROOT = ROOT + "/cache"
CACHE_TRADINGLOG = CACHE_ROOT + "/tradinglog.pkl"
CACHE_TRADINGLOG_HISTORY = CACHE_ROOT + "/tradinglog-history.pkl"

DASH_ASSETS = ROOT + "/assets"

CACHE_COLORS = CACHE_ROOT + "/position-colors.pkl"
