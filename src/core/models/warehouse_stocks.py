from pydantic import BaseModel

from core.models.stocks_by_sku import StocksBySku

__all__ = ('WarehouseStocks',)


class WarehouseStocks(BaseModel):
    warehouse_id: int
    category: str
    stocks: list[StocksBySku]
