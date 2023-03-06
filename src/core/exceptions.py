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


class WildberriesAPIError(Exception):

    def __init__(self, *args, response: httpx.Response):
        super().__init__(*args)
        self.response = response


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
