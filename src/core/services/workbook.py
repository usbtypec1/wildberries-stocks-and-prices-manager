import contextlib
import pathlib
from zipfile import BadZipFile

import openpyxl
from openpyxl.workbook import Workbook

from core.exceptions import WorkbookValidationError

__all__ = ('closing_workbook',)


@contextlib.contextmanager
def closing_workbook(file_path: pathlib.Path) -> Workbook:
    if not file_path.exists():
        raise WorkbookValidationError(
            message=f'Файл {file_path.name} отсутствует',
        )

    try:
        workbook: Workbook = openpyxl.load_workbook(file_path)
    except BadZipFile:
        raise WorkbookValidationError(
            message=(
                f'Файл {file_path.name} поврежден или имеет неверный формат'
            ),
        )

    with contextlib.closing(workbook):
        yield workbook
