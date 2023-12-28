from pydantic import BaseModel

__all__ = ('WarehouseStocksRow',)


class WarehouseStocksRow(BaseModel):
    warehouse_id: int
    sku: str
    stocks_amount: int
