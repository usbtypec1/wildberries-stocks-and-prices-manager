from pydantic import BaseModel

__all__ = ('StocksBySku',)


class StocksBySku(BaseModel):
    sku: str
    amount: int
