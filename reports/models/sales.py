from datetime import datetime

from pydantic.dataclasses import dataclass


@dataclass
class Item:
    name: str
    qtd: float
    unity_price: float
    discount: float = 0


@dataclass
class Sale:
    date: datetime
    total_value: float
    items: list[Item]
