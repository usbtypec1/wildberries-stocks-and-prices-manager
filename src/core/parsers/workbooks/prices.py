from collections.abc import Iterable
from typing import TypeAlias

from openpyxl.cell import Cell
from openpyxl.workbook import Workbook
from pydantic import ValidationError

from core.exceptions import WorkbookValidationError
from core.models import NomenclaturePriceToUpdate
from core.parsers.workbooks.common import get_worksheet_by_name

__all__ = ('parse_prices_workbook',)

Row: TypeAlias = Iterable[Cell]
Rows: TypeAlias = Iterable[Row]


def parse_row(row: Row) -> NomenclaturePriceToUpdate:
    nomenclature_id, price = [cell.value for cell in row]

    try:
        return NomenclaturePriceToUpdate(
            nomenclature_id=nomenclature_id,
            price=price,
        )
    except ValidationError:
        raise WorkbookValidationError(message='Неправильные nm ID или цена')


def parse_prices_workbook(
        workbook: Workbook,
) -> list[NomenclaturePriceToUpdate]:
    worksheet = get_worksheet_by_name(
        workbook=workbook,
        name='Цены',
    )
    rows: Rows = worksheet['A2': f'B{worksheet.max_row}']
    return [parse_row(row) for row in rows]
