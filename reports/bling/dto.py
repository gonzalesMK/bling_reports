from datetime import datetime
from pydantic import BaseModel, validator


def convert_price(price: str):
    return price.replace(",", ".")


class BlingItem(BaseModel):
    codigo: str
    descricao: str
    quantidade: float
    valorunidade: float
    descontoItem: float

    _normalize_quantidade = validator("quantidade", allow_reuse=True, pre=True)(
        convert_price
    )
    _normalize_valor_unidade = validator("valorunidade", allow_reuse=True, pre=True)(
        convert_price
    )
    _normalize_desconto_item = validator("descontoItem", allow_reuse=True, pre=True)(
        convert_price
    )


class ItemWrapper(BaseModel):
    item: BlingItem


class BlingSale(BaseModel):
    desconto: float
    data: datetime
    totalvenda: float
    totalprodutos: float
    itens: list[ItemWrapper]

    _normalize_desconto = validator("desconto", allow_reuse=True, pre=True)(
        convert_price
    )
    _normalize_total_venda = validator("totalvenda", allow_reuse=True, pre=True)(
        convert_price
    )
    _normalize_total_produtos = validator("totalprodutos", allow_reuse=True, pre=True)(
        convert_price
    )

    @validator("data", pre=True)
    def str_to_date(cls, date: str):
        return datetime.strptime(date, "%Y-%m-%d")


class SaleWrapper(BaseModel):
    pedido: BlingSale


class Sales(BaseModel):
    pedidos: list[SaleWrapper]


class GetSales(BaseModel):
    retorno: Sales
