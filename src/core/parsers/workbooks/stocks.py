from collections import defaultdict
from collections.abc import Iterable
from typing import TypeAlias

from openpyxl.cell import Cell
from openpyxl.workbook import Workbook
from pydantic import ValidationError

from core.exceptions import WorkbookValidationError
from core.models import WarehouseStocks, StocksBySku, WarehouseStocksRow
from core.parsers.workbooks.common import get_worksheet_by_name

StocksBySkus: TypeAlias = list[StocksBySku]
GroupedStocks: TypeAlias = defaultdict[int, StocksBySkus]

__all__ = ('parse_stocks_workbook',)


def map_warehouse_stocks(
        stocks_grouped_by_warehouse_id: GroupedStocks,
) -> list[WarehouseStocks]:
    return [
        WarehouseStocks(
            warehouse_id=warehouse_id,
            stocks=stocks_by_sku,
            category='',
        ) for warehouse_id, stocks_by_sku in
        stocks_grouped_by_warehouse_id.items()
    ]


def parse_row(row: Iterable[Cell], row_number: int) -> WarehouseStocksRow:
    try:
        warehouse_id, sku, stocks_amount = [cell.value for cell in row]
    except ValueError:
        raise WorkbookValidationError(
            message=f'Неправильное количество данных в строке №{row_number}'
        )

    try:
        return WarehouseStocksRow(
            warehouse_id=warehouse_id,
            sku=sku,
            stocks_amount=stocks_amount,
        )
    except ValidationError:
        raise WorkbookValidationError(
            message='Неправильный формат данных в строке №{row_number}'
        )


def parse_stocks_by_sku(
        row: WarehouseStocksRow,
        row_number: int,
) -> StocksBySku:
    try:
        return StocksBySku(
            sku=row.sku,
            amount=row.stocks_amount,
        )
    except ValidationError:
        raise WorkbookValidationError(
            message=(
                'Неправильные sku или количество остатков:'
                f' Строка {row_number}'
            )
        )


def group_stocks_by_warehouse_id(
        rows: Iterable[Iterable[Cell]],
) -> GroupedStocks:
    stocks_grouped_by_warehouse_id: GroupedStocks = defaultdict(list)

    for row_number, row in enumerate(rows, start=2):
        row = parse_row(row, row_number)
        stocks_by_sku = parse_stocks_by_sku(row, row_number)
        stocks_grouped_by_warehouse_id[row.warehouse_id].append(stocks_by_sku)

    return stocks_grouped_by_warehouse_id


def parse_stocks_workbook(workbook: Workbook) -> list[WarehouseStocks]:
    worksheet = get_worksheet_by_name(
        workbook=workbook,
        name='Остатки',
    )
    rows = worksheet['A2': f'C{worksheet.max_row}']
    stocks_grouped_by_warehouse_id = group_stocks_by_warehouse_id(rows)

    return map_warehouse_stocks(stocks_grouped_by_warehouse_id)
