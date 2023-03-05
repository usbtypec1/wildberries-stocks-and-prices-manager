from pydantic import BaseModel, PositiveInt

__all__ = (
    'StockToUpdate',
    'WarehouseStocks',
    'NomenclaturePriceToUpdate',
)


class StockToUpdate(BaseModel):
    sku: str
    amount: int


class WarehouseStocks(BaseModel):
    warehouse_id: int
    stocks: list[StockToUpdate]


class NomenclaturePriceToUpdate(BaseModel):
    nomenclature_id: int
    price: PositiveInt
