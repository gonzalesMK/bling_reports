#!/usr/bin/env python
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

from dateutil.relativedelta import relativedelta, SU
from dataclasses import dataclass
import csv

from bling_reports.bling.bling_api import BlingClient


class ItemInfo:
    qtd: float = 0
    value: float = 0


@dataclass
class WeeklyItemSale:
    week: str
    item_info: dict[str, ItemInfo]


DATE_FORMAT = "%d/%m/%Y"


def load_data(client: BlingClient, n_weeks=4) -> dict[str, ItemInfo]:
    """
    Report :

    Product | Week 1 | Week 2 | ...
    abc     | 100    | 200    | 300
    """
    dates = _get_week_dates(datetime.today(), n_weeks=n_weeks)

    reports = {}
    for end_date, start_date in dates:
        sales = client.list_sales(start_date, end_date)

        # Group by Products
        item_info = defaultdict(lambda: [0, 0])

        for sale in sales:
            for it in sale.items:
                item_info[it.name][0] += it.qtd
                item_info[it.name][1] += it.qtd * (it.unity_price - it.discount)

        reports[f"{start_date.strftime(DATE_FORMAT)}"] = item_info

    return reports


def _transpose(report: dict[str, dict[str, ItemInfo]]):
    remmaped = defaultdict(lambda: defaultdict(lambda: [0]))
    for key, value in report.items():
        for inner_key, inner_value in value.items():
            remmaped[inner_key][key] = inner_value
    return remmaped


def to_csv(report: dict[str, dict[str, list[str]]], path: Path):
    """
    Report should be a dict with  "column" them "row" then a list of values
    """
    remmaped = _transpose(report)
    columns = [r for r in report.keys()]

    with open(path, mode="w") as csvfile:
        print("csvfile")
        writer = csv.writer(csvfile, delimiter=";")
        writer.writerow(["produtos"] + columns)

        values = [
            [key, *map(lambda x: x[0], [values[c] for c in columns])]
            for key, values in remmaped.items()
        ]
        writer.writerows(values)


def _get_week_dates(start_date: datetime, n_weeks=4) -> list[tuple[datetime, datetime]]:
    dates = []
    tmp_date = start_date
    for i in range(n_weeks):
        week_end = tmp_date - timedelta(days=1) + relativedelta(weekday=SU(-1))
        dates.append((tmp_date, week_end))
        tmp_date = week_end

    return dates


if __name__ == "__main__":
    from os import getenv

    client = BlingClient(getenv("BLING_API_KEY"))
    report_data = load_data(client, n_weeks=4)
    to_csv(report_data, "sales_report.csv")
