import collections
import pathlib
from typing import DefaultDict

import openpyxl

from core import models
from core.helpers import grouper
from core.parser import WorkbookParser
from core.services.http_clients import closing_wildberries_api_http_client
from core.services.wildberries_api import WildberriesAPIService
from core.templates import Template


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
                wildberries_api_service.update_stocks(warehouse_stocks.warehouse_id, stocks_group)


def download_prices(api_key: str):
    with closing_wildberries_api_http_client(api_key=api_key) as http_client:
        wildberries_api_service = WildberriesAPIService(http_client)

        nomenclature_prices = wildberries_api_service.get_prices(models.QuantityStatus.ANY)

    with Template('./выгрузка цен.xlsx') as template:
        template.add_prices_rows(nomenclature_prices)


def download_stocks(api_key: str):
    warehouse_id_to_stocks_by_skus: DefaultDict[int, list[models.StockToUpdate]] = collections.defaultdict(list)
    skus: set[str] = set()

    with closing_wildberries_api_http_client(api_key=api_key) as http_client:
        wildberries_api_service = WildberriesAPIService(http_client)
        warehouses = wildberries_api_service.get_warehouses()

        for nomenclatures in wildberries_api_service.get_nomenclatures():
            skus |= {
                sku
                for nomenclature in nomenclatures
                for size in nomenclature['sizes']
                for sku in size['skus']
                if sku
            }

        for skus_group in grouper(skus, n=1000):
            for warehouse in warehouses:
                stocks_by_skus = wildberries_api_service.get_stocks_by_skus(warehouse_id=warehouse.id,
                                                                            skus=skus_group)
                if stocks_by_skus:
                    warehouse_id_to_stocks_by_skus[warehouse.id] += stocks_by_skus
                    break

    warehouses_stocks = [
        models.WarehouseStocks(warehouse_id=warehouse_id, stocks=stocks_by_skus)
        for warehouse_id, stocks_by_skus in warehouse_id_to_stocks_by_skus.items()
    ]
    with Template('./выгрузка остатков.xlsx') as template:
        template.add_stocks_rows(warehouses_stocks)
