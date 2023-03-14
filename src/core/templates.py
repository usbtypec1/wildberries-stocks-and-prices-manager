import contextlib
import pathlib
from typing import Iterable

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

from core import models


def generate_template_file(file_path: pathlib.Path) -> None:
    workbook = openpyxl.Workbook(write_only=True)

    with contextlib.closing(workbook):
        prices_worksheet: Worksheet = workbook.create_sheet('Цены')
        prices_worksheet.append(('nm ID', 'Новая цена'))

        stocks_worksheet: Worksheet = workbook.create_sheet('Остатки')
        stocks_worksheet.append(('ID склада', 'sku', 'Количество остатков'))

        workbook.save(file_path)


def generate_prices_report_file(
        *,
        file_path: pathlib.Path,
        categories_prices: Iterable[models.CategoryPrices],
) -> None:
    workbook = openpyxl.Workbook(write_only=True)

    with contextlib.closing(workbook):
        worksheet: Worksheet = workbook.create_sheet('Цены')
        worksheet.append(('Категория товара', 'nm ID', 'Новая цена', 'Скидка'))

        for category_prices in categories_prices:

            for nomenclature_price in category_prices.nomenclature_prices:
                worksheet.append((
                    category_prices.category_name,
                    nomenclature_price.nomenclature_id,
                    nomenclature_price.price,
                    nomenclature_price.discount,
                ))

        workbook.save(file_path)


def generate_stocks_report_file(
        *,
        file_path: pathlib.Path,
        warehouses_stocks: Iterable[models.WarehouseStocks],
) -> None:
    workbook = openpyxl.Workbook(write_only=True)

    with contextlib.closing(workbook):
        worksheet: Worksheet = workbook.create_sheet('Остатки')
        worksheet.append(('ID склада', 'Категория', 'sku', 'Количество остатков'))

        for warehouse_stocks in warehouses_stocks:
            for stock in warehouse_stocks.stocks:
                worksheet.append((warehouse_stocks.warehouse_id, warehouse_stocks.category, stock.sku, stock.amount))

        workbook.save(file_path)
