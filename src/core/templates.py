import logging
import pathlib
from typing import Iterable

import openpyxl
from openpyxl.cell import WriteOnlyCell
from openpyxl.worksheet.worksheet import Worksheet

from core import models


class Template:

    def __init__(self, file_path: str | pathlib.Path):
        self.__file_path = file_path
        self.__workbook = openpyxl.Workbook()
        self.__prices_worksheet: Worksheet = self.__workbook.create_sheet('Цены')
        self.__stocks_worksheet: Worksheet = self.__workbook.create_sheet('Остатки')
        self.__write_headers()
        self.__is_saved = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()
        self.__workbook.close()

    def save(self):
        if not self.__is_saved:
            self.__workbook.save(self.__file_path)
            logging.debug(f'Template file was created in {self.__file_path}')
            self.__is_saved = True

    def __write_headers(self):
        self.__prices_worksheet.append(('nm ID', 'Цена'))
        self.__stocks_worksheet.append(('ID склада', 'sku', 'Количество остатков'))

    def add_prices_row(self, nomenclature_prices: Iterable[models.NomenclaturePrice]) -> None:
        for nomenclature_price in nomenclature_prices:
            self.__prices_worksheet.append((nomenclature_price.nomenclature_id, nomenclature_price.price))

    def add_stocks_row(self, warehouses_stocks: Iterable[models.WarehouseStocks]) -> None:
        for warehouse_stocks in warehouses_stocks:
            for stock in warehouse_stocks.stocks:
                self.__stocks_worksheet.append((warehouse_stocks.warehouse_id, stock.sku, stock.amount))
