from pydantic import BaseModel

from core.models.wildberries_api import NomenclaturePrice

__all__ = ('CategoryPrices',)


class CategoryPrices(BaseModel):
    category_name: str
    nomenclature_prices: list[NomenclaturePrice]
