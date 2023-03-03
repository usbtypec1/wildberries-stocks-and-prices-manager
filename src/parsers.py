from typing import TypeAlias

from openpyxl.cell import ReadOnlyCell
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from pydantic import ValidationError

import models

PricesWorksheetRow: TypeAlias = tuple[ReadOnlyCell, ReadOnlyCell, ReadOnlyCell]
StocksWorksheetRow: TypeAlias = tuple[ReadOnlyCell, ReadOnlyCell, ReadOnlyCell, ReadOnlyCell]


class WorkbookParser:

    def __init__(self, workbook: Workbook):
        self.__workbook = workbook

    def parse_stocks_worksheet(self) -> models.ParsedStocksWorksheet:
        worksheet: Worksheet = self.__workbook['Остатки']
        rows: tuple[StocksWorksheetRow, ...] = worksheet['A2': f'D{worksheet.max_row}']

        parsed_rows: list[models.StocksWorksheetRow] = []
        error_row_numbers: list[int] = []

        for row_number, row in enumerate(rows, start=2):
            shop_name, warehouse_id, sku, stocks_amount = [cell.value for cell in row]

            try:
                parsed_row = models.StocksWorksheetRow(
                    shop_name=shop_name,
                    warehouse_id=warehouse_id,
                    sku=sku,
                    stocks_amount=stocks_amount
                )
            except ValidationError:
                error_row_numbers.append(row_number)
            else:
                parsed_rows.append(parsed_row)

        return models.ParsedStocksWorksheet(rows=parsed_rows, error_row_numbers=error_row_numbers)
