from unittest import TestCase
from datetime import datetime
import requests
import json
from pathlib import Path
import responses

from reports.bling.bling_api import BlingClient
from reports.models.sales import Sale, Item

TEST_FOLDER = Path(__file__).parent.parent / "resources"

MOCKED_RESULT = [
    Sale(
        date=datetime(2017, 7, 28, 0, 0),
        total_value=428.9,
        items=[
            Item(name="Caneta 001", qtd=120.0, unity_price=1.68, discount=0.0),
            Item(name="Caderno Capa 102", qtd=20.0, unity_price=9.9, discount=0.0),
        ],
    )
]


class TestBlingClient(TestCase):
    def test_list_sales_works(self):
        with open(TEST_FOLDER / "example_list_sales_response.json") as file:
            body = file.read()
        with open(TEST_FOLDER / "bling_no_resource_found.json") as file:
            body_end = file.read()

        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            url = requests.utils.quote(
                "https://bling.com.br/Api/v2/pedidos/page=1/json/?filters=dataEmissao[12/12/2013"
                " TO 05/02/2014];idSituacao[6,9]&apikey=123",
                safe="!#$%&'()*+,/:;=?@~",
            )

            url_2 = requests.utils.quote(
                "https://bling.com.br/Api/v2/pedidos/page=2/json/?filters=dataEmissao[12/12/2013"
                " TO 05/02/2014];idSituacao[6,9]&apikey=123",
                safe="!#$%&'()*+,/:;=?@~",
            )
            rsps.get(
                url,
                status=200,
                body=body,
            )
            rsps.get(
                url_2,
                status=200,
                body=body_end,
            )

            start_date = datetime(year=2013, month=12, day=12)
            end_date = datetime(year=2014, month=2, day=5)
            client = BlingClient(api_key="123")
            response = client.list_sales(
                start_date=start_date, end_date=end_date, status=[6, 9]
            )
            assert len(response) == 1
            assert response[0].json() == MOCKED_RESULT[0].json()
