from dataclasses import dataclass

from pydantic import BaseModel

__all__ = (
    'SupplierCredentialsWorksheetRow',
    'ParsedSupplierCredentialsWorksheet',
)


class SupplierCredentialsWorksheetRow(BaseModel):
    shop_name: str
    api_key: str


@dataclass(frozen=True, slots=True)
class ParsedSupplierCredentialsWorksheet:
    rows: list[SupplierCredentialsWorksheetRow]
    error_row_numbers: list[int]
