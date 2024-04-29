from typing import Literal

# Default values of the scope buttons
indexByTakeTime: Literal[0, 1] = 0
scopeByIndex: Literal[0, 1] = 1
calcWithOpens: Literal[0, 1] = 1

# Column specifications
logColOrder: list[int] = [
    1,  # Asset Ids
    2,  # Invest
    3,  # Take
    4,  # ITC
    5,  # Result
    6,  # Note
    7,  # Hold Time
    8,  # Hypotheses
]
logColWidths: list[int] = [
    140,  # 0  Name
    0,    # 1  Symbol (recommended to set to 70 if the symbol plugin is implemented)
    0,    # 2  Type
    80,   # 3  n
    170,  # 4  InvestTime
    150,  # 5  InvestAmount
    110,  # 6  InvestCourse
    170,  # 7  TakeTime
    150,  # 8  TakeAmount
    110,  # 9  TakeCourse
    80,   # 10 ITC
    110,  # 11 Profit
    110,  # 12 Performance
    80,   # 13 Dividend
    120,  # 14 Note
    170,  # 15 HoldTime
    160,  # 16 Profit/Day
    160,  # 17 Performance/Day
]

# Default values for the visibility of columns in the `balance` section.
balanceT52W: Literal[0, 1] = 1
balanceCurrent: Literal[0, 1] = 1
balanceYears: Literal[0, 1] = 1
balanceQuarters: Literal[0, 1] = 1

# Miscellaneous values for the `statistic` section.
#   Performance diagrams
#       Calculation (week | month | quarters)
statisticsPerformanceStepsDefault: Literal["w", "m", "q"] = "w"
statisticsPerformanceIntervalDefault: Literal["w", "m", "q"] = "w"
statisticsPerformanceFrameDefault: Literal["w", "m", "q"] = "q"
#       Range (months)
statisticsPerformanceRangeDefault: Literal[0, 12, 24, 48] = 0
#       Performance Graphs Order             # (how diagrams are merged)
statisticsPerformanceOrder: list[int] = [    # statisticsPerformanceOrder: list[int] = [
    1,  # Trading Profit & Performance       #     1,  # Trading Profit & Performance
    2,  # Summary Profit & Rate              #     1,  # Summary Profit & Rate
    3,  # Deposits, Payouts & Money          #     2,  # Deposits, Payouts & Money
    4,  # Trading Amount                     #     3,  # Trading Amount
    5,  # Ø Profit/Day, Ø Perf./Day          #     4,  # Ø Profit/Day, Ø Perf./Day
    6,  # ~Amount, ~Ø Perf.                  #     5,  # ~Amount, ~Ø Perf.
    7,  # ~Ø Profit/Day, ~Ø Perf./Day        #     6,  # ~Ø Profit/Day, ~Ø Perf./Day
    8,  # ~Activity, ~Ø Hold Days            #     7,  # ~Activity, ~Ø Hold Days
]                                            # ]
#   Positions diagrams
#       Group by ...
statisticsGroupByType: Literal[0, 1] = 0  # else by ID
statisticsIdBySymbol: Literal[0, 1] = 0   # else ID = Name
#       Color cache  # (delete the cachefile to reset the cache)
statisticsUsePositionColorCache: Literal[0, 1] = 1
#   Layouts
statisticsPerformanceGraphSize: int = 1000
statisticsPopGraphSize: int = 2000
statisticsOpenPositionsGraphSize: int = 500
statisticsAllPositionsGraphSize: int = 500
statisticsSunMaxDepth: int = 4


# Upper limit of history entries
nHistorySlots: int = 10

# Window grid options
#   Whether the `balance` section should be shown at startup instead of the `statistics` section.
sideInitBalance: Literal[0, 1] = 0
#   Set the following configuration to `0` if none of the sections should be shown at startup.
gridSideSizeInitScale: float = 0.2  # 0 ... 1
gridDefWidthScale: float = 0.2  # 0 ... 1
gridMinWidthScale: float = 0.1  # 0 ... 1
gridRow3Height: int = 120
bottomBarDistanceBottom: int = 105
bottomBarDistanceRight: int = 10

# Activation and specification of an interval for the course plugin.
# Only useful if the corresponding plugin is implemented.
# The program can significantly lose performance, especially if `with_open`
# is enabled and one of the sections `statistic` or `balance` is open,
# as these are recalculated.
coursePluginUpdateInterval: Literal[0, 1] = 0
coursePluginUpdateIntervalOn: Literal[0, 1] = 0
coursePluginUpdateIntervalMs: int = 10_000

# Display change deltas
cellRendererChangeTakeAmount: Literal[0, 1] = 0
cellRendererChangeTakeCourse: Literal[0, 1] = 0
cellRendererChangePerformance: Literal[0, 1] = 1
cellRendererChangeProfit: Literal[0, 1] = 1

# misc
startupFlushOpenTakeAmount: Literal[0, 1] = 1
useDefaultAltColors: Literal[0, 1] = 0  # So far, this only affects the columns `Performance` and `Profit`
disableCopyPaste: Literal[0, 1] = 0
disableFooterLifeSignal: Literal[0, 1] = 1
dateFormat: Literal["ISO 8601", "american", "international", "ydm", "mdy", "dmy"] = "international"
dateFormatFirstDayOfWeek = 1  # 0=Sunday
