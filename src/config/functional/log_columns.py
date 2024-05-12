from src.config import rc
from src.config.styles.log import *


dataTypeDefinitions = {
    'percentage': {
        'extendsDataType': 'number',
        'baseDataType': 'number',
        "valueFormatter": {"function": "params.value == null ? '' :  d3.format('+,.2%')(params.value)"},
        "columnTypes": "rightAligned",
        "appendColumnTypes": True
    },
    'percentage3': {
        'extendsDataType': 'number',
        'baseDataType': 'number',
        "valueFormatter": {"function": "params.value == null ? '' :  d3.format('+,.3%')(params.value)"},
        "columnTypes": "rightAligned",
        "appendColumnTypes": True
    },
    'prefixed': {
        'extendsDataType': 'number',
        'baseDataType': 'number',
        "valueFormatter": {"function": "params.value == null ? '' :  d3.format('+,.2f')(params.value)"},
        "columnTypes": "rightAligned",
        "appendColumnTypes": True
    },
    'prefixed3': {
        'extendsDataType': 'number',
        'baseDataType': 'number',
        "valueFormatter": {"function": "params.value == null ? '' :  d3.format('+,.3f')(params.value)"},
        "columnTypes": "rightAligned",
        "appendColumnTypes": True
    },
    'grouped': {
        'extendsDataType': 'number',
        'baseDataType': 'number',
        "valueFormatter": {"function": "params.value == null ? '' :  d3.format(',.2f')(params.value)"},
        "columnTypes": "rightAligned",
        "appendColumnTypes": True
    },
    'timedelta': {
        'extendsDataType': 'number',
        'baseDataType': 'number',
        "columnTypes": "rightAligned",
        "appendColumnTypes": True
    },
}


_calcCell = {
    "valueFormatter": {"function": "params.value == null ? '' :  d3.format(',.2f')(params.value)"},
    "valueParser": {"function": "calc(params.newValue)"},
}


Name = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == ''",
                "style": name_undefined,
            },
            {
                "condition": "params.data.cat == 'd' && params.data.Note",
                "style": name_DEPOSIT_tag | name_has_note,
            },
            {
                "condition": "params.data.cat == 'p' && params.data.Note",
                "style": name_PAYOUT_tag | name_has_note,
            },
            {
                "condition": "params.data.cat == 'i' && params.data.Note",
                "style": name_ITC_tag | name_has_note,
            },
            {
                "condition": "params.data.cat == 'd'",
                "style": name_DEPOSIT_tag,
            },
            {
                "condition": "params.data.cat == 'p'",
                "style": name_PAYOUT_tag,
            },
            {
                "condition": "params.data.cat == 'i'",
                "style": name_ITC_tag,
            },
            {
                "condition": "params.data.cat == 'v' && params.data.Note",
                "style": name_dividend | name_has_note,
            },
            {
                "condition": "params.data.cat == 'v'",
                "style": name_dividend,
            },
            {
                "condition": "params.data.cat == 'to' && params.data.Note && params.data.Dividend",
                "style": name_opentrade | name_has_note | name_has_dividend,
            },
            {
                "condition": "params.data.cat == 'to'  && params.data.Dividend",
                "style": name_opentrade | name_has_dividend,
            },
            {
                "condition": "params.data.cat == 'to' && params.data.Note",
                "style": name_opentrade | name_has_note,
            },
            {
                "condition": "params.data.cat == 'to'",
                "style": name_opentrade,
            },
            {
                "condition": "params.data.Note",
                "style": name_has_note,
            },
            {
                "condition": "params.data.Dividend",
                "style": name_has_dividend,
            },
            {
                "condition": "params.data.cat == 'tf'",
                "style": name_finalized_trade,
            },
        ],
        "defaultStyle": name_undefined,
    },
    "width": rc.logColWidths[0],
    "hide": not rc.logColWidths[0]
}

Symbol = {
    'cellStyle': {} | symbol,
    "width": rc.logColWidths[1],
    "hide": not rc.logColWidths[1]
}

Type = {
    'cellStyle': {} | type,
    "width": rc.logColWidths[2],
    "hide": not rc.logColWidths[2]
}

N = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.value == 0",
                "style": n_special,
            },
            {
                "condition": "params.value < 0",
                "style": n_ignore,
            },
        ],
        "defaultStyle": n_default,
    },
    "width": rc.logColWidths[3],
    "hide": not rc.logColWidths[3]
}

InvestTime = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == 'd' && params.data.InvestAmount == params.data.TakeAmount + params.data.ITC",
                "style": invest_deposit_null,
            },
            {
                "condition": "params.data.cat == ''",
                "style": invest_col | undefined,
            },
            {
                "condition": "params.data.cat == 'd'",
                "style": invest_deposit,
            },
            {
                "condition": "params.data.cat == 'p'",
                "style": invest_payout,
            },
            {
                "condition": "params.data.cat == 'i'",
                "style": invest_itc,
            },
            {
                "condition": "params.data.cat == 'v'",
                "style": invest_dividend,
            },
        ],
        "defaultStyle": invest_col,
    },
    "width": rc.logColWidths[4],
    "hide": not rc.logColWidths[4]
}

InvestAmount = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == 'd'",
                "style": invest_amount_deposit,
            },
        ] + InvestTime["cellStyle"]["styleConditions"],
        "defaultStyle": invest_col,
    },
    "width": rc.logColWidths[5],
    "hide": not rc.logColWidths[5]
} | _calcCell

InvestCourse = InvestTime | {"width": rc.logColWidths[6], "hide": not rc.logColWidths[6]} | _calcCell

TakeTime = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == 'd' && params.data.InvestAmount == params.data.TakeAmount + params.data.ITC",
                "style": take_deposit_null,
            },
            {
                "condition": "params.data.cat == ''",
                "style": take_col | undefined,
            },
            {
                "condition": "params.data.cat == 'd'",
                "style": take_deposit,
            },
            {
                "condition": "params.data.cat == 'p'",
                "style": take_payout,
            },
            {
                "condition": "params.data.cat == 'i'",
                "style": take_itc,
            },
            {
                "condition": "params.data.cat == 'v'",
                "style": take_dividend,
            },
        ],
        "defaultStyle": take_col,
    },
    "width": rc.logColWidths[7],
    "hide": not rc.logColWidths[7]
}

TakeAmount = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == 'p'",
                "style": take_amount_payout,
            },
            {
                "condition": "params.data.cat == 'v'",
                "style": take_amount_dividend,
            },
        ] + TakeTime["cellStyle"]["styleConditions"],
        "defaultStyle": take_col,
    },
    "width": rc.logColWidths[8],
    "hide": not rc.logColWidths[8]
} | rc.cellRendererChangeTakeAmount | _calcCell

TakeCourse = TakeTime | {"width": rc.logColWidths[9], "hide": not rc.logColWidths[9]} | rc.cellRendererChangeTakeCourse | _calcCell


Itc = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == ''",
                "style": itc_col | undefined,
            },
            {
                "condition": "params.data.cat == 'i'",
                "style": itc_itc,
            },
            {
                "condition": "params.data.cat == 'v'",
                "style": itc_dividend,
            },
            {
                "condition": "params.data.cat == 'p'",
                "style": itc_payout,
            },
            {
                "condition": "params.data.cat == 'd'",
                "style": itc_deposit,
            },
        ],
        "defaultStyle": itc_col,
    },
    "width": rc.logColWidths[10],
    "hide": not rc.logColWidths[10]
} | _calcCell

Performance = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == 'i'",
                "style": performance_itc,
            },
            {
                "condition": "params.data.cat == 'p'",
                "style": performance_payout,
            },
            {
                "condition": "params.data.cat == 'd' && params.value > 0",
                "style": performance_pos_deposit,
            },
            {
                "condition": "params.data.cat == 'd' && params.value <= 0",
                "style": performance_neg_deposit,
            },
            {
                "condition": "params.data.cat == 'v'",
                "style": result_dividend,
            },
            {
                "condition": "params.value > 0",
                "style": performance_pos,
            },
        ],
        "defaultStyle": performance_neg,
    },
    "width": rc.logColWidths[12],
    "hide": not rc.logColWidths[12]
} | rc.cellRendererChangePerformance

Profit = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == 'd' && params.value > 0",
                "style": profit_pos_deposit,
            },
            {
                "condition": "params.data.cat == 'd' && params.value <= 0",
                "style": profit_neg_deposit,
            },
            {
                "condition": "params.value > 0",
                "style": profit_pos,
            },
        ],
        "defaultStyle": profit_neg,
    },
    "width": rc.logColWidths[11],
    "hide": not rc.logColWidths[11]
} | rc.cellRendererChangeProfit

Dividend = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.data.cat == 'd'",
                "style": result_deposit,
            },
        ],
        "defaultStyle": result,
    },
    "width": rc.logColWidths[13],
    "hide": not rc.logColWidths[13]
}

Note = {
    'cellStyle': {"white-space": "pre"} | note,
    "width": rc.logColWidths[14],
    "hide": not rc.logColWidths[14]
}

HoldTime = {
    'cellStyle': holdtime,
    "width": rc.logColWidths[15],
    "hide": not rc.logColWidths[15]
}

ProfitDay = {
    'cellStyle': {
        "styleConditions": [
            {
                "condition": "params.value > 0",
                "style": statistic_pos,
            },
        ],
        "defaultStyle": statistic_neg,
    },
    "width": rc.logColWidths[16],
    "hide": not rc.logColWidths[16]
}

PerformanceDay = ProfitDay | {"width": rc.logColWidths[17], "hide": not rc.logColWidths[17]}
