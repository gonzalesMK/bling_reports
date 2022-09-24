from unittest import TestCase
from reports.reports.weekly_sales import _get_week_dates

from datetime import datetime

DATE_FORMAT = "%d/%m/%Y"


class TestWeeklyReport(TestCase):
    def test_week_dates(self):
        start_date = datetime(year=2022, month=9, day=24)
        dates = _get_week_dates(start_date=start_date, n_weeks=2)

        dates = [(s.strftime(DATE_FORMAT), b.strftime(DATE_FORMAT)) for s, b in dates]
        assert dates == [("24/09/2022", "18/09/2022"), ("18/09/2022", "11/09/2022")]
