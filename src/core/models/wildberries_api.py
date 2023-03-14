import datetime
from enum import IntEnum

from pydantic import BaseModel, Field, validator

__all__ = (
    'QuantityStatus',
    'NomenclaturePrice',
    'Warehouse',
    'StocksBySku',
    'NomenclatureSize',
    'Nomenclature',
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


class StocksBySku(BaseModel):
    sku: str
    amount: int


class NomenclatureSize(BaseModel):
    tech_size: str = Field(alias='techSize')
    skus: list[str]

    @validator('skus')
    def filter_empty_skus(cls, value: list[str]) -> list[str]:
        return [sku for sku in value if sku]


class Nomenclature(BaseModel):
    sizes: list[NomenclatureSize]
    media_files: list[str] = Field(alias='mediaFiles')
    colors: list[str]
    update_at: datetime.datetime = Field(alias='updateAt')
    vendor_code: str = Field(alias='vendorCode')
    brand: str
    object: str
    id: int = Field(alias='nmID')
