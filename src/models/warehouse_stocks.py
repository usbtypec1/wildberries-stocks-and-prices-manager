from pydantic import BaseModel

from models.stocks_by_sku import StocksBySku

__all__ = ('WarehouseStocks',)


class WarehouseStocks(BaseModel):
    warehouse_id: int
    stocks: list[StocksBySku]
