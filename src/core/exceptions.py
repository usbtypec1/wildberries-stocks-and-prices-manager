from dataclasses import dataclass

import httpx


class ValidationError(Exception):
    pass


class WorksheetMissingError(ValidationError):

    def __init__(self, *args, worksheet_name: str):
        super().__init__(*args)
        self.worksheet_name = worksheet_name


class WorkbookValidationError(ValidationError):

    def __init__(self, *args, worksheet_name: str, row_number: int):
        super().__init__(*args)
        self.worksheet_name = worksheet_name
        self.row_number = row_number


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
