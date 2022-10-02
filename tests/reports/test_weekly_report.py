from unittest import TestCase
from unittest.mock import patch, mock_open
import json
from pathlib import Path
from datetime import datetime
import requests
import responses
from freezegun import freeze_time
from reports.reports.weekly_sales import _get_week_dates, load_data, to_csv
from reports.bling.bling_api import BlingClient


DATE_FORMAT = "%d/%m/%Y"
TEST_FOLDER = Path(__file__).parent.parent / "bling"


def mock_url_pedidos(start_date: datetime, end_date: datetime, page: int = None):
    start_str = start_date.strftime("%d/%m/%Y")
    end_str = end_date.strftime("%d/%m/%Y")
    page_str = "/page={page}" if page else ""
    url = requests.utils.quote(
        f"https://bling.com.br/api/v2/pedidos{page_str}/json/?filters=dataEmissao[{start_str} TO"
        f" {end_str}];idSituacao[6,9]&apikey=123",
        safe="!#$%&'()*+,/:;=?@~",
    )
    return url


def mock_response(rsps):
    with open(TEST_FOLDER / "example_list_sales_response.json") as file:
        body = file.read()

    start_date = datetime.today()
    dates = _get_week_dates(start_date=start_date, n_weeks=2)
    for start, end in dates:
        url = mock_url_pedidos(start, end)
        rsps.get(url, body=body)

    client = BlingClient(api_key="123")
    return client


MOCKED_REPORT_DATA = {
    "01/10/2022-25/09/2022": {
        "Caneta 001": [120.0, 201.6],
        "Caderno Capa 102": [20.0, 198.0],
    },
    "25/09/2022-18/09/2022": {
        "Caneta 001": [120.0, 201.6],
        "Caderno Capa 102": [20.0, 198.0],
    },
}


MOCKED_REPORT_DATA_MISSING_PRODUCT = {
    "01/10/2022-25/09/2022": {
        "Caneta 001": [120.0, 201.6],
    },
    "25/09/2022-18/09/2022": {
        "Caneta 001": [120.0, 201.6],
        "Caderno Capa 102": [20.0, 198.0],
    },
}


class TestWeeklyReport(TestCase):
    def test_week_dates(self):
        start_date = datetime(year=2022, month=9, day=24)
        dates = _get_week_dates(start_date=start_date, n_weeks=2)

        dates = [(s.strftime(DATE_FORMAT), b.strftime(DATE_FORMAT)) for s, b in dates]
        assert dates == [("24/09/2022", "18/09/2022"), ("18/09/2022", "11/09/2022")]

    def test_load_data(self):
        start_date = datetime(year=2022, month=10, day=1)
        with freeze_time(start_date), responses.RequestsMock() as rsps:
            client = mock_response(rsps)
            reports = load_data(client, n_weeks=2)
            assert json.dumps(reports) == json.dumps(MOCKED_REPORT_DATA)

    def test_to_csv(self):
        m = mock_open()
        with patch("builtins.open", m):
            to_csv(MOCKED_REPORT_DATA, path="some_path")

        m.assert_called_once_with("some_path", mode="w")
        handle = m().write
        calls = handle.mock_calls
        handle.assert_called_with("Caderno Capa 102;20.0;20.0\r\n")

        assert (
            calls[0].args[0]
            == "produtos;01/10/2022-25/09/2022;25/09/2022-18/09/2022\r\n"
        )

    def test_to_csv_missing(self):
        m = mock_open()
        with patch("builtins.open", m):
            to_csv(MOCKED_REPORT_DATA_MISSING_PRODUCT, path="some_path")

        m.assert_called_once_with("some_path", mode="w")
        handle = m().write
        calls = handle.mock_calls
        handle.assert_called_with("Caderno Capa 102;0;20.0\r\n")
