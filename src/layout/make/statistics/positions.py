from functools import cached_property
from typing import Literal

import plotly.graph_objects as go

from src.calc.log import LogCalc, _Trade
from src.config import styles, rc

_colorPalette = styles.figures.color_palette_donut.copy()


class _Positions:
    new_calc: bool
    lc: LogCalc
    group_by: Literal["name", "symbol", "type/name", "type/symbol"] | str

    open_ids: list
    open_labels: list
    open_parents: list
    open_values: list
    open_colors: list

    all_ids: list
    all_labels: list
    all_parents: list
    all_values: list
    all_colors: list

    open_figure: go.Figure
    all_figure: go.Figure

    def __init__(self, lc: LogCalc, group_by: Literal["name", "symbol", "type/name", "type/symbol"] | str = "name"):
        self.lc = lc
        self.opt__group_by(group_by)

    def opt__group_by(self, group_by: Literal["name", "symbol", "type/name", "type/symbol"] | str):
        self.group_by = group_by
        self.new_calc = True

    def get(self):
        if self.new_calc:
            self.new_calc = False

            __colorPalette = _colorPalette.copy()
            __colorCache = dict()

            def get_color(_key):
                nonlocal __colorPalette
                try:
                    return __colorCache[_key]
                except KeyError:
                    try:
                        color = __colorPalette.pop(0)
                    except IndexError:
                        __colorPalette = _colorPalette.copy()
                        color = __colorPalette.pop(0)
                    __colorCache[_key] = color
                    return color

            labels = []
            values = []
            parents = []
            ids = []
            colors = []

            class Asset:
                id: str
                trades: list[_Trade]
                amount: float
                color: str

                def __init__(self, id: str, color: str):
                    self.id = id
                    self.trades = list()
                    self.amount = 0
                    self.color = color

                def add(self, obj):
                    self.trades.append(obj)
                    self.amount += obj.amount

            if self.group_by.startswith("type"):

                class Group:
                    id: str
                    assets: dict[str, Asset]
                    color: str

                    @cached_property
                    def amount(self) -> float:
                        return sum(a.amount for a in self.assets.values())

                    def __init__(self, id: str, color: str):
                        self.id = id
                        self.assets = dict()
                        self.color = color

                    def add(self, asset: Asset):
                        self.assets[asset.id] = asset

                    def reset(self):
                        del self.amount

                if self.group_by.endswith("name"):
                    c_key = "Name"
                else:
                    c_key = "Symbol"

                groups = dict()

                def make(trades):
                    nonlocal labels, values, parents, ids, colors

                    for g in groups.values():
                        g.reset()

                    for opn in reversed(trades):
                        typ = opn.row_dat.get("Type")
                        c_id = opn.row_dat.get(c_key)
                        try:
                            group = groups[typ]
                        except KeyError:
                            color = get_color(c_id)
                            asset = Asset(c_id, color)
                            color = get_color(typ)
                            group = Group(typ, color)
                            groups[typ] = group
                            asset.add(opn)
                            group.add(asset)
                        else:
                            try:
                                asset = group.assets[c_id]
                            except KeyError:
                                color = get_color(c_id)
                                asset = Asset(c_id, color)
                                asset.add(opn)
                                group.add(asset)
                            else:
                                asset.add(opn)

                    total_value = sum(g.amount for g in groups.values())
                    total_label = f"{len(groups)}<br>{total_value:,.2f}"
                    labels = [total_label]
                    values = [total_value]
                    parents = [""]
                    ids = [_main_id := "-1"]
                    colors = [""]

                    n = 0
                    for g_id, g_item in groups.items():
                        parents.append(_main_id)
                        ids.append(_g_id := f"{n}")
                        g_label = (f"{g_id}<br>"
                                   f"{g_item.amount:,.2f} ( {g_item.amount / total_value:,.2%} )")
                        labels.append(g_label)
                        values.append(g_item.amount)
                        colors.append(g_item.color)
                        nn = 0
                        for a_id, a_item in g_item.assets.items():
                            parents.append(_g_id)
                            ids.append(_a_id := f"{n}/{nn}")
                            a_label = (f"{a_id}<br>"
                                       f"{a_item.amount:,.2f} ( {a_item.amount / g_item.amount:,.2%} )")
                            labels.append(a_label)
                            values.append(a_item.amount)
                            colors.append(a_item.color)
                            nnn = 0
                            for trade in a_item.trades:
                                parents.append(_a_id)
                                ids.append(f"{n}/{nn}/{nnn}")
                                t_label = (f"{a_id}<br>"
                                           f"{trade.amount:,.2f} ( {trade.amount / a_item.amount:,.2%} )")
                                labels.append(t_label)
                                values.append(trade.amount)
                                colors.append(a_item.color)
                                nnn += 1
                            nn += 1
                        n += 1

            else:
                if self.group_by == "name":
                    key = "Name"
                else:
                    key = "Symbol"

                assets = dict()

                def make(trades):
                    nonlocal labels, values, parents, ids, colors
                    for opn in reversed(trades):
                        c_id = opn.row_dat.get(key)
                        try:
                            asset = assets[c_id]
                        except KeyError:
                            color = get_color(c_id)
                            asset = Asset(c_id, color)
                            assets[c_id] = asset

                        asset.add(opn)

                    total_value = sum(a.amount for a in assets.values())
                    total_label = f"{len(assets)}<br>{total_value:,.2f}"

                    labels = [total_label]
                    values = [total_value]
                    parents = [""]
                    ids = [_main_id := "-1"]
                    colors = [""]

                    for n, _a_item in enumerate(assets.items()):
                        a_id, a_item = _a_item
                        parents.append(_main_id)
                        ids.append(_id := f"{n}")
                        a_label = (f"{a_id}<br>"
                                   f"{a_item.amount:,.2f} ( {a_item.amount / total_value:,.2%} )")
                        labels.append(a_label)
                        values.append(a_item.amount)
                        colors.append(a_item.color)
                        for nn, trade in enumerate(a_item.trades):
                            parents.append(_id)
                            ids.append(f"{n}/{nn}")
                            t_label = (f"{a_id}<br>"
                                       f"{trade.amount:,.2f} ( {trade.amount / a_item.amount:,.2%} )")
                            labels.append(t_label)
                            values.append(trade.amount)
                            colors.append(a_item.color)

            make(self.lc.open_trades)

            self.open_ids = ids
            self.open_labels = labels
            self.open_parents = parents
            self.open_values = values
            self.open_colors = colors

            self.open_figure = go.Figure(
                go.Sunburst(
                    ids=ids,
                    labels=labels,
                    parents=parents,
                    values=values,
                    branchvalues="total",
                    maxdepth=rc.statisticsSunMaxDepth,
                    marker=dict(colors=colors),
                    hovertemplate="%{label}<extra></extra>"
                ),
            )

            make(self.lc.fin_trades)

            self.all_ids = ids
            self.all_labels = labels
            self.all_parents = parents
            self.all_values = values
            self.all_colors = colors

            self.all_figure = go.Figure(
                go.Sunburst(
                    ids=ids,
                    labels=labels,
                    parents=parents,
                    values=values,
                    branchvalues="total",
                    maxdepth=rc.statisticsSunMaxDepth,
                    marker=dict(colors=colors),
                    hovertemplate="%{label}<extra></extra>"
                ),
            )

            self.open_figure.update_layout(
                dict(plot_bgcolor="#2d3436", paper_bgcolor="#2d3436"),
                font=dict(color='#dedddc'),
                margin=dict(t=0, l=0, r=0, b=0),
            )

            self.all_figure.update_layout(
                dict(plot_bgcolor="#2d3436", paper_bgcolor="#2d3436"),
                font=dict(color='#dedddc'),
                margin=dict(t=0, l=0, r=0, b=0),
            )

        return self.open_figure, self.all_figure

    @staticmethod
    def new(
            lc: LogCalc,
            group_by: Literal["name", "symbol", "type/name", "type/symbol"] | str
    ):
        global OBJ
        OBJ = _Positions(lc, group_by)
        return OBJ


OBJ: _Positions = _Positions


