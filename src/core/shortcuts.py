import logging
import pathlib

import openpyxl

from core.helpers import grouper
from core.parser import WorkbookParser
from core.services.http_clients import closing_wildberries_api_http_client
from core.services.wildberries_api import WildberriesAPIService


def run(api_key: str, workbook_file_path: str | pathlib.Path):
    workbook = openpyxl.load_workbook(workbook_file_path, read_only=True)

    parser = WorkbookParser(workbook)
    nomenclature_prices = parser.get_prices()
    warehouses_stocks = parser.get_stocks()

    with closing_wildberries_api_http_client(api_key=api_key) as http_client:
        wildberries_api_service = WildberriesAPIService(http_client)

        for nomenclature_prices_group in grouper(nomenclature_prices, n=1000):
            wildberries_api_service.update_prices(nomenclature_prices_group)

        for warehouse_stocks in warehouses_stocks:
            for stocks_group in grouper(warehouse_stocks.stocks, n=100):
                try:
                    wildberries_api_service.update_stocks(warehouse_stocks.warehouse_id, stocks_group)
                except Exception:
                    logging.exception('Error while updating stocks')
