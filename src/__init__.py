from re import sub

ROOT = sub("[^/\\\\]+$", "", __file__)

CACHE_ROOT = ROOT + "/cache"
CACHE_TRADINGLOG = CACHE_ROOT + "/tradinglog.pkl"
CACHE_TRADINGLOG_HISTORY = CACHE_ROOT + "/tradinglog-history.pkl"

DASH_ASSETS = ROOT + "/assets"

CACHE_COLORS = CACHE_ROOT + "/position-colors.pkl"

FILE_CLONES = DASH_ASSETS + "/fc"
FILE_CLONES_URL = "./assets/fc"
FILE_CLONES_FLUSH_TIMESTAMP = CACHE_ROOT + "/.fc.timestamp"
FILE_CLONES_TRASH = CACHE_ROOT + "/.fc.trash"
