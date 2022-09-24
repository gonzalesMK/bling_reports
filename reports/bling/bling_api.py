from requests import get
from datetime import datetime
from .dto import GetSales
from reports.models.sales import Sale, Item

SALES_ENDPOINT = "https://bling.com.br/Api/v2/pedidos/json/"

DATE_FORMAT = "%d/%m/%Y"


class BlingClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def list_sales(
        self, start_date: datetime, end_date: datetime, status: list[int]
    ) -> list[Sale]:
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

        bling_sales = GetSales.parse_obj(response.json())

        return self._bling_sales_to_model(bling_sales)

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
