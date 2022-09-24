from unittest import TestCase
from datetime import datetime
import requests
import json
from pathlib import Path
import responses

from reports.bling.bling_api import BlingClient


TEST_FOLDER = Path(__file__).parent


class TestBlingClient(TestCase):
    def test_list_sales_works(self):
        with open(TEST_FOLDER / "example_list_sales_response.json") as file:
            body = file.read()

        with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
            url = requests.utils.quote(
                "https://bling.com.br/Api/v2/pedidos/json/?filters=dataEmissao[12/12/2013"
                " TO 05/02/2014];idSituacao[6,9]&apikey=123",
                safe="!#$%&'()*+,/:;=?@~",
            )

            rsps.get(
                url,
                status=200,
                body=body,
            )
            start_date = datetime(year=2013, month=12, day=12)
            end_date = datetime(year=2014, month=2, day=5)
            client = BlingClient(api_key="123")
            response = client.list_sales(
                start_date=start_date, end_date=end_date, status=[6, 9]
            )
