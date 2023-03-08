import collections
from typing import TypeAlias, DefaultDict

from openpyxl.cell.read_only import ReadOnlyCell
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from pydantic import ValidationError

import core.models.wildberries_api
from core import exceptions, models

__all__ = ('WorkbookParser',)

StocksWorksheetRow: TypeAlias = tuple[ReadOnlyCell, ReadOnlyCell, ReadOnlyCell, ReadOnlyCell]
PricesWorksheetRow: TypeAlias = tuple[ReadOnlyCell, ReadOnlyCell, ReadOnlyCell]


class WorkbookParser:

    def __init__(self, workbook: Workbook):
        self.__workbook = workbook

    def __get_worksheet(self, name: str) -> Worksheet:
        try:
            return self.__workbook[name]
        except KeyError:
            raise exceptions.WorksheetMissingError(worksheet_name=name)

    def get_stocks(self) -> list[models.WarehouseStocks]:
        worksheet = self.__get_worksheet('Остатки')

        rows: tuple[StocksWorksheetRow, ...] = worksheet['A2': f'C{worksheet.max_row}']

        warehouse_id_to_stocks_to_update: DefaultDict[int, list[
            core.models.wildberries_api.StocksBySku]] = collections.defaultdict(list)
        for row_number, row in enumerate(rows, start=2):
            warehouse_id, sku, stocks_amount = [cell.value for cell in row]
            try:
                int(warehouse_id)
            except (ValueError, TypeError):
                raise exceptions.WorkbookValidationError(
                    'ID склада должно быть числом',
                    worksheet_name='Остатки',
                    row_number=row_number,
                )

            try:
                stock_to_update = core.models.wildberries_api.StocksBySku(sku=sku, amount=stocks_amount)
            except ValidationError:
                raise exceptions.WorkbookValidationError(
                    'Неправильные sku или количество остатков',
                    worksheet_name='Остатки',
                    row_number=row_number,
                )
            else:
                warehouse_id_to_stocks_to_update[warehouse_id].append(stock_to_update)

        warehouses_stocks: list[models.WarehouseStocks] = [
            models.WarehouseStocks(warehouse_id=warehouse_id, stocks=stocks_to_update)
            for warehouse_id, stocks_to_update in warehouse_id_to_stocks_to_update.items()
        ]
        return warehouses_stocks

    def get_prices(self) -> list[models.NomenclaturePriceToUpdate]:
        worksheet = self.__get_worksheet('Цены')

        rows: tuple[PricesWorksheetRow, ...] = worksheet['A2': f'B{worksheet.max_row}']

        nomenclature_prices: list[models.NomenclaturePriceToUpdate] = []
        for row_number, row in enumerate(rows, start=2):
            nomenclature_id, price = [cell.value for cell in row]

            try:
                nomenclature_price = models.NomenclaturePriceToUpdate(nomenclature_id=nomenclature_id, price=price)
            except ValidationError:
                raise exceptions.WorkbookValidationError(
                    'Неправильные nm ID или цена',
                    worksheet_name='Остатки',
                    row_number=row_number,
                )
            else:
                nomenclature_prices.append(nomenclature_price)

        return nomenclature_prices
