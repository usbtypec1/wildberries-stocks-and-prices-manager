from pydantic import BaseModel, PositiveInt

from core.models.wildberries_api import StocksBySku

__all__ = (
    'WarehouseStocks',
    'NomenclaturePriceToUpdate',
)


class WarehouseStocks(BaseModel):
    warehouse_id: int
    stocks: list[StocksBySku]


class NomenclaturePriceToUpdate(BaseModel):
    nomenclature_id: int
    price: PositiveInt
