import models
from parsers import WorkbookParser


def test_parse_valid_api_keys_worksheet(workbook_with_valid_api_keys_worksheet):
    parser = WorkbookParser(workbook_with_valid_api_keys_worksheet)
    expected = models.ParsedSupplierCredentialsWorksheet(
        rows=[
            models.SupplierCredentialsWorksheetRow(
                shop_name='kukmin',
                api_key='tEcSDHRgTPlXZjMr8SB5WqCkPac1FmIcoOA7RbXXlReqAnKAfK',
            ),
            models.SupplierCredentialsWorksheetRow(
                shop_name='Bobnik',
                api_key='cwhZxVGdf4yt9h86oNwusvFj0zjTv8dF4DR09FsvG0QN40Ceb2',
            ),
            models.SupplierCredentialsWorksheetRow(
                shop_name='Mylo',
                api_key='iY5aODc9scrLFijZ6fqQru7jQM1rYvu9B2aEZT97ZH4B0uFtYq'
            ),
            models.SupplierCredentialsWorksheetRow(
                shop_name='Myshka',
                api_key='ViFIiuk5t6k9423JXYipyzvrQ9ux7DF6lFvVMZ0V7C3yzL2e8B',
            ),
        ],
        error_row_numbers=[],
    )
    assert parser.parse_api_keys_worksheet() == expected


def test_parse_api_keys_worksheet_with_invalid_rows(workbook_with_invalid_api_keys_worksheet):
    parser = WorkbookParser(workbook_with_invalid_api_keys_worksheet)
    expected = models.ParsedSupplierCredentialsWorksheet(
        rows=[
            models.SupplierCredentialsWorksheetRow(
                shop_name='kukmin',
                api_key='tEcSDHRgTPlXZjMr8SB5WqCkPac1FmIcoOA7RbXXlReqAnKAfK',
            ),
            models.SupplierCredentialsWorksheetRow(
                shop_name='Myshka',
                api_key='ViFIiuk5t6k9423JXYipyzvrQ9ux7DF6lFvVMZ0V7C3yzL2e8B',
            ),
        ],
        error_row_numbers=[3, 4],
    )
    assert parser.parse_api_keys_worksheet() == expected
