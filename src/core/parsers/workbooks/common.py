from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from core.exceptions import WorksheetMissingError

__all__ = ('get_worksheet_by_name',)


def get_worksheet_by_name(*, workbook: Workbook, name: str) -> Worksheet:
    try:
        return workbook[name]
    except KeyError:
        raise WorksheetMissingError(worksheet_name=name)
