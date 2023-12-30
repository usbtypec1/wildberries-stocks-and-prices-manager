from pydantic import BaseModel, ConfigDict

__all__ = ('WarehouseStocksRow',)


class WarehouseStocksRow(BaseModel):
    warehouse_id: int
    sku: str
    stocks_amount: int

    model_config = ConfigDict(coerce_numbers_to_str=True)
