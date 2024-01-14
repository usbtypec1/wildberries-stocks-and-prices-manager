from pydantic import BaseModel

from models.nomenclature_prices import NomenclaturePrice

__all__ = ('CategoryPrices',)


class CategoryPrices(BaseModel):
    category_name: str
    nomenclature_prices: list[NomenclaturePrice]
