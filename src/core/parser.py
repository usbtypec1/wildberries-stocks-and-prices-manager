from typing import TypeAlias

from openpyxl.cell.read_only import ReadOnlyCell
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from pydantic import ValidationError

from core import exceptions, models

__all__ = ('WorkbookParser',)

StocksWorksheetRow: TypeAlias = tuple[
    ReadOnlyCell, ReadOnlyCell, ReadOnlyCell, ReadOnlyCell]
PricesWorksheetRow: TypeAlias = tuple[ReadOnlyCell, ReadOnlyCell, ReadOnlyCell]


class WorkbookParser:

    def __init__(self, workbook: Workbook):
        self.__workbook = workbook

    def __get_worksheet(self, name: str) -> Worksheet:
        try:
            return self.__workbook[name]
        except KeyError:
            raise exceptions.WorksheetMissingError(worksheet_name=name)

    def get_prices(self) -> list[models.NomenclaturePriceToUpdate]:
        worksheet = self.__get_worksheet('Цены')

        rows: tuple[PricesWorksheetRow, ...] = worksheet[
                                               'A2': f'B{worksheet.max_row}']

        nomenclature_prices: list[models.NomenclaturePriceToUpdate] = []
        for row_number, row in enumerate(rows, start=2):
            nomenclature_id, price = [cell.value for cell in row]

            try:
                nomenclature_price = models.NomenclaturePriceToUpdate(
                    nomenclature_id=nomenclature_id, price=price)
            except ValidationError:
                raise exceptions.WorkbookValidationError(
                    'Неправильные nm ID или цена',
                    worksheet_name='Остатки',
                    row_number=row_number,
                )
            else:
                nomenclature_prices.append(nomenclature_price)

        return nomenclature_prices
