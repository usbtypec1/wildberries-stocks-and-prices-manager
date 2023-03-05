from openpyxl.cell import ReadOnlyCell
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from core import exceptions, models

__all__ = ('WorkbookParser',)


class WorkbookParser:

    def __init__(self, workbook: Workbook):
        self.__workbook = workbook

    def get_suppliers_credentials(self) -> list[models.SupplierCredentials]:
        try:
            worksheet: Worksheet = self.__workbook['Ключи']
        except KeyError:
            raise exceptions.WorksheetMissingError(worksheet_name='Ключи')

        rows: tuple[tuple[ReadOnlyCell, ReadOnlyCell], ...] = worksheet['A2': F'B{worksheet.max_row}']

        shop_name_to_api_key: dict[str, str] = {}
        for row in rows:
            shop_name_cell, api_key_cell = row

            if not (shop_name := str(shop_name_cell.value)):
                raise exceptions.WorkbookValidationError(
                    'Отсутствует название магазина',
                    worksheet_name='Ключи',
                    row_number=shop_name_cell.row,
                    column_number=shop_name_cell.column,
                )

            if not (api_key := str(shop_name_cell.value)):
                raise exceptions.WorkbookValidationError(
                    'Отсутствует API ключ',
                    worksheet_name='Ключи',
                    row_number=api_key_cell.row,
                    column_number=api_key_cell.column,
                )

            if shop_name in shop_name_to_api_key:
                raise exceptions.WorkbookValidationError(
                    'Дублирующиеся названия магазинов',
                    worksheet_name='Ключи',
                    row_number=shop_name_cell.row,
                    column_number=shop_name_cell.column,
                )

            shop_name_to_api_key[shop_name] = api_key

        return [
            models.SupplierCredentials(shop_name=shop_name, api_key=api_key)
            for shop_name, api_key in shop_name_to_api_key.items()
        ]

    def get_stocks(self):
        pass

    def get_prices(self):
        pass
