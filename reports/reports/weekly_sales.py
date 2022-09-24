#!/usr/bin/env python
from reports.bling.bling_api import BlingClient
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, SU, SA

from dataclasses import dataclass
from collections import defaultdict


class ItemInfo:
    qtd: float = 0
    value: float = 0


@dataclass
class WeeklyItemSale:
    week: str

    item_info: dict[str, ItemInfo]


def generate(client: BlingClient, n_weeks=4):
    dates = _get_week_dates(datetime.today())

    reports = []
    for start_date, end_date in dates:
        sales = client.list_sales(start_date, end_date)

        # Group by Products
        item_info = defaultdict(ItemInfo)

        for sale in sales:
            for it in sale.items:
                item_info[it.name].qtd += it.qtd
                item_info[it.name].value += it.qtd * (it.unity_price - it.discount)

        reports.append(WeeklyItemSale(week=end_date, item_info=item_info))

    return reports


def _get_week_dates(start_date: datetime, n_weeks=4):
    dates = []
    tmp_date = start_date
    for i in range(n_weeks):
        week_end = tmp_date - timedelta(days=1) + relativedelta(weekday=SU(-1))
        dates.append((tmp_date, week_end))
        tmp_date = week_end

    return dates


# client = BlingClient(api_key="123")
# client.list_sales()
