from dataclasses import dataclass

from pydantic import BaseModel

__all__ = (
    'StocksWorksheetRow',
    'ParsedStocksWorksheet',
    'StockToUpdate',
)


class StocksWorksheetRow(BaseModel):
    shop_name: str
    warehouse_id: int
    sku: str
    stocks_amount: int


@dataclass(frozen=True, slots=True)
class ParsedStocksWorksheet:
    rows: list[StocksWorksheetRow]
    error_row_numbers: list[int]


class StockToUpdate(BaseModel):
    sku: str
    amount: int
