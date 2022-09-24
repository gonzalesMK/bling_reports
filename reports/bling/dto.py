from pydantic import BaseModel, validator, Field


def convert_price(price: str):
    return price.replace(",", ".")


class Item(BaseModel):
    codigo: str
    descricao: str
    quantidade: str
    valorunidade: str
    descontoItem: str

    _normalize_quantidade = validator("quantidade", allow_reuse=True)(convert_price)
    _normalize_valor_unidade = validator("valorunidade", allow_reuse=True)(
        convert_price
    )
    _normalize_desconto_item = validator("descontoItem", allow_reuse=True)(
        convert_price
    )


class ItemWrapper(BaseModel):
    item: Item


class Sale(BaseModel):
    desconto: str
    data: str
    totalvenda: str
    totalprodutos: str
    itens: list[ItemWrapper]

    _normalize_desconto = validator("desconto", allow_reuse=True)(convert_price)
    _normalize_total_venda = validator("totalvenda", allow_reuse=True)(convert_price)
    _normalize_total_produtos = validator("totalprodutos", allow_reuse=True)(
        convert_price
    )


class SaleWrapper(BaseModel):
    pedido: Sale


class Sales(BaseModel):
    pedidos: list[SaleWrapper]


class GetSales(BaseModel):
    retorno: Sales
