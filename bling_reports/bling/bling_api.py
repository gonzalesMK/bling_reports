from requests import get
from datetime import datetime
from .dto import GetSales
from ..models.sales import Sale, Item

SALES_ENDPOINT = "https://bling.com.br/Api/v2/pedidos/"

DATE_FORMAT = "%d/%m/%Y"


class BlingClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def list_sales(
        self, start_date: datetime, end_date: datetime, status: list[int] = [6, 9]
    ) -> list[Sale]:
        """
        Filter the sales from start_date and end_date (included)
        """
        sales = []
        for i in range(1, 100, 1):
            url = self._make_url(start_date, end_date, status, self.api_key, page=i)
            response = get(url)

            if response.status_code == 403:
                print(response.text)
                raise ValueError("Wrong status code")

            bling_sales = GetSales.parse_obj(response.json())

            if hasattr(bling_sales.retorno, "erros"):
                if bling_sales.retorno.erros[0].erro.cod != 14:
                    print(bling_sales)
                break
            sales += self._bling_sales_to_model(bling_sales)

        return sales

    @staticmethod
    def _make_url(
        start_date: datetime,
        end_date: datetime,
        status: list[int],
        api_key: str,
        page: int,
    ):
        data_filter = (
            f"dataEmissao[{start_date.strftime(DATE_FORMAT)} TO"
            f" {end_date.strftime(DATE_FORMAT)}]"
        )
        situation_filter = f"idSituacao[{','.join([str(s) for s in status])}]"
        api_key = f"apikey={api_key}"

        page_str = f"page={page}/" if page else ""
        format_str = "json/"
        url = (
            SALES_ENDPOINT
            + page_str
            + format_str
            + "?filters="
            + data_filter
            + ";"
            + situation_filter
            + "&"
            + api_key
        )
        return url

    @staticmethod
    def _bling_sales_to_model(bling_sales: GetSales) -> list[Sale]:
        sales = []
        for sale_wrapper in bling_sales.retorno.pedidos:
            sale = sale_wrapper.pedido

            sale = Sale(
                date=sale.data,
                total_value=sale.totalvenda,
                items=[
                    Item(
                        name=i.item.descricao,
                        qtd=i.item.quantidade,
                        unity_price=i.item.valorunidade,
                        discount=i.item.descontoItem,
                    )
                    for i in sale.itens
                ],
            )
            sales.append(sale)

        return sales
