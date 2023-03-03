import models
from parsers import WorkbookParser


def test_stocks_worksheet_parser(workbook_only_with_valid_stocks_worksheet):
    parser = WorkbookParser(workbook_only_with_valid_stocks_worksheet)
    expected = models.ParsedStocksWorksheet(
        rows=[
            models.StocksWorksheetRow(
                shop_name='Kukmin',
                warehouse_id=12345,
                sku='314774612483966',
                stocks_amount=1000,
            ),
            models.StocksWorksheetRow(
                shop_name='Kukmin',
                warehouse_id=12345,
                sku='438410461799342',
                stocks_amount=1000,
            ),
            models.StocksWorksheetRow(
                shop_name='Kukmin',
                warehouse_id=12345,
                sku='736050367978036',
                stocks_amount=1000,
            ),
            models.StocksWorksheetRow(
                shop_name='Kukmin',
                warehouse_id=12345,
                sku='737925783485028',
                stocks_amount=1000,
            ),
        ],
        error_row_numbers=[],
    )
    assert parser.parse_stocks_worksheet() == expected


def test_stocks_worksheet_with_invalid_rows(workbook_with_invalid_stocks_worksheet):
    parser = WorkbookParser(workbook_with_invalid_stocks_worksheet)
    expected = models.ParsedStocksWorksheet(
        rows=[
            models.StocksWorksheetRow(
                shop_name='Kukmin',
                warehouse_id=12345,
                sku='314774612483966',
                stocks_amount=1000,
            ),
        ],
        error_row_numbers=[3, 4, 5, 6],
    )
    assert parser.parse_stocks_worksheet() == expected
