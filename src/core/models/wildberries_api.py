from enum import IntEnum

from pydantic import BaseModel, Field

__all__ = (
    'QuantityStatus',
    'NomenclaturePrice',
    'Warehouse',
)


class QuantityStatus(IntEnum):
    ANY = 0
    ONLY_WITH_STOCKS = 1
    ONLY_WITHOUT_STOCKS = 2


class NomenclaturePrice(BaseModel):
    nomenclature_id: int = Field(alias='nmId')
    price: int
    discount: int
    promocode: int = Field(alias='promoCode')


class Warehouse(BaseModel):
    id: int
    name: str
