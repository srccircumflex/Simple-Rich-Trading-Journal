import dash_ag_grid as dag

from src.config import rc, color_theme
from src.config.functional import log_columns

__debug = 0


_columns_ = [
    {
        "headerName": "Asset",
        "children": [
            {
                "field": "Name",
                "pinned": "left",
                "filter": "agTextColumnFilter",
                "filterParams": {"buttons": ["clear"]},
                "headerTooltip": None
            } | log_columns.Name,
            {
                "field": "cat",
                "hide": not __debug,
                "width": 50
            },
            {
                "field": "id",
                "hide": not __debug,
                "width": 50
            }
        ]
    },
    {
        "headerName": "",
        "children": [
            {
                "field": "Symbol",
                "filter": "agTextColumnFilter",
                "filterParams": {"buttons": ["clear"]},
                "headerTooltip": None,
            } | log_columns.Symbol,
            {
                "field": "Type",
                "filter": "agTextColumnFilter",
                "filterParams": {"buttons": ["clear"]},
                "headerTooltip": None,
            } | log_columns.Type,
            {
                "field": "n",
                "headerName": "n",
                "type": "rightAligned",
                "cellDataType": "number",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
            } | log_columns.N,
        ]
    },
    {
        "headerName": "Invest",
        "children": [
            {
                "field": "InvestTime",
                "headerName": "Time",
                "filter": "agDateColumnFilter",
                "filterParams": {
                    "comparator": {"function": "dateFilterComparator"},
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["equals", "greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "type": "rightAligned",
            } | log_columns.InvestTime,
            {
                "field": "InvestAmount",
                "headerName": "Amount",
                "type": "rightAligned",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
            } | log_columns.InvestAmount,
            {
                "field": "InvestCourse",
                "headerName": "Course",
                "type": "rightAligned",
                "editable": True,
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
            } | log_columns.InvestCourse,
        ]
    },
    {
        "headerName": "Take",
        "children": [
            {
                "field": "TakeTime",
                "headerName": "Time",
                "filter": "agDateColumnFilter",
                "filterParams": {
                    "comparator": {"function": "dateFilterComparator"},
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["equals", "greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "type": "rightAligned",
            } | log_columns.TakeTime,
            {
                "field": "TakeAmount",
                "headerName": "Amount",
                "type": "rightAligned",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
            } | log_columns.TakeAmount,
            {
                "field": "TakeCourse",
                "headerName": "Course",
                "type": "rightAligned",
                "editable": True,
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
            } | log_columns.TakeCourse,
        ]
    },
    {
        "field": "ITC",
        "headerName": "+ITC",
        "type": "rightAligned",
        "filterParams": {
            "buttons": ["clear"],
            "defaultOption": "greaterThan",
            "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
        },
        "headerTooltip": "Costs, Interests, Taxes ..."
    } | log_columns.Itc,
    {
        "headerName": "Result",
        "children": [
            {
                "field": "Performance",
                "type": "rightAligned",
                "editable": False,
                "cellDataType": "percentage",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
            } | log_columns.Performance,
            {
                "field": "Profit",
                "type": "rightAligned",
                "editable": False,
                "cellDataType": "prefixed",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
            } | log_columns.Profit,
            {
                "field": "Dividend",
                "type": "rightAligned",
                "editable": False,
                "cellDataType": "grouped",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
            } | log_columns.Dividend,
        ]
    },
    {
        "field": "Note",
        "filter": "agTextColumnFilter",
    } | log_columns.Note,
    {
        "field": "HoldTime",
        "headerName": "Hold Time",
        "type": "rightAligned",
        "editable": False,
        "cellDataType": "timedelta",
        "filter": "agNumberColumnFilter",
        "filterParams": {
            "allowedCharPattern": "\\d\\|\\., ",
            "filterPlaceholder": "y | m | d | H , M",
            "numberParser": {"function": "timedeltaParser(params)"},
            "numberFormatter": {"function": "timedeltaFormatter(params)"},
            "buttons": ["clear"],
            "defaultOption": "greaterThan",
            "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
        },
        "valueFormatter": {"function": "timedeltaFormatter(params.value)"},
        "headerTooltip": "y | m | d | H , M"
    } | log_columns.HoldTime,
    {
        "headerName": "Hypotheses",
        "children": [
            {
                "field": "Performance/Day",
                "type": "rightAligned",
                "editable": False,
                "cellDataType": "percentage3",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "headerTooltip": "Performance / (rounded 24h or 1)"
            } | log_columns.PerformanceDay,
            {
                "field": "Profit/Day",
                "type": "rightAligned",
                "editable": False,
                "cellDataType": "prefixed3",
                "filterParams": {
                    "buttons": ["clear"],
                    "defaultOption": "greaterThan",
                    "filterOptions": ["greaterThan", "lessThan", "greaterThanOrEqual", "lessThanOrEqual", "inRange"],
                },
                "headerTooltip": "Profit / (rounded 24h or 1)"
            } | log_columns.ProfitDay,
        ]
    },
]

__columns = [_columns_[0]] + ([None] * len(rc.logColOrder))

for i, o in enumerate(rc.logColOrder, 1):
    __columns[o] = _columns_[i]

del _columns_

_default_col_def = {
    "editable": True,
    "filter": "agNumberColumnFilter",
    "filterParams": {"buttons": ["clear"]},
    "cellEditorParams": {"color": "white"}
}

_dashGridOptions = {
    "dataTypeDefinitions": log_columns.dataTypeDefinitions,
    "tooltipShowDelay": 0,
    "undoRedoCellEditing": True,
    "undoRedoCellEditingLimit": 20,
}

tradinglog = dag.AgGrid(
    id="tradinglog_",
    columnDefs=__columns,
    defaultColDef=_default_col_def,
    dashGridOptions=_dashGridOptions,
    getRowId="params.data.id",
    className=color_theme.table_theme + " ag-alt-colors",
    dangerously_allow_code=True,
    style={
        "height": "100%",
        "width": "100%",
        "fontSize": "13px"
    },
)
