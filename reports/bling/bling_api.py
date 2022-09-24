from requests import get
from datetime import datetime
from .dto import GetSales

SALES_ENDPOINT = "https://bling.com.br/Api/v2/pedidos/json/"

DATE_FORMAT = "%d/%m/%Y"


class BlingClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def list_sales(
        self, start_date: datetime, end_date: datetime, status: list[int]
    ) -> GetSales:
        """
        Filter the sales from start_date and end_date (included)
        """

        data_filter = (
            f"dataEmissao[{start_date.strftime(DATE_FORMAT)} TO"
            f" {end_date.strftime(DATE_FORMAT)}]"
        )
        situation_filter = f"idSituacao[{','.join([str(s) for s in status])}]"
        api_key = f"apikey={self.api_key}"

        url = (
            SALES_ENDPOINT
            + "?filters="
            + data_filter
            + ";"
            + situation_filter
            + "&"
            + api_key
        )
        response = get(url)

        return GetSales.parse_obj(response.json())
