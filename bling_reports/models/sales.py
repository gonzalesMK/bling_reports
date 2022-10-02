from datetime import datetime

from pydantic import BaseModel


class Item(BaseModel):
    name: str
    qtd: float
    unity_price: float
    discount: float = 0


class Sale(BaseModel):
    date: datetime
    total_value: float
    items: list[Item]
