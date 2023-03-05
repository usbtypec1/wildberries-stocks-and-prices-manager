class ValidationError(Exception):
    pass


class WorksheetMissingError(ValidationError):

    def __init__(self, *args, worksheet_name: str):
        super().__init__(*args)
        self.worksheet_name = worksheet_name


class WorkbookValidationError(ValidationError):

    def __init__(self, *args, worksheet_name: str, row_number: int, column_number: int):
        super().__init__(*args)
        self.worksheet_name = worksheet_name
        self.row_number = row_number
        self.column_number = column_number
