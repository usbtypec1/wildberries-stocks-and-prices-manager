from dataclasses import dataclass

import httpx


class ValidationError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class WorksheetMissingError(ValidationError):
    worksheet_name: str

    def __str__(self):
        return f'Worksheet {self.worksheet_name!r} is missing'


@dataclass(frozen=True, slots=True)
class WorkbookValidationError(ValidationError):
    message: str

    def __str__(self):
        return f'Workbook validation error: {self.message}'


@dataclass(frozen=True, slots=True)
class WildberriesAPIError(Exception):
    response: httpx.Response

    def __str__(self):
        return (
            f'Wildberries API error: {self.response.status_code=}\n'
            f'Response: {self.response.text}'
        )


class UnauthorizedError(WildberriesAPIError):
    pass


class BadRequestError(WildberriesAPIError):
    pass


class PermissionDeniedError(WildberriesAPIError):
    pass


class NotFoundError(WildberriesAPIError):
    pass


class StocksUpdateError(WildberriesAPIError):
    pass


class TooManyRequestsError(WildberriesAPIError):
    pass


class WarehousesDoNotExistError(WildberriesAPIError):
    pass
