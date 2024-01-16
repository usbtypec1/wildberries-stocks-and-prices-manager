import contextlib
import pathlib
from collections.abc import Generator

from fast_depends import Depends, inject
from openpyxl.workbook import Workbook
from rich import get_console
from rich.console import Console
from rich.progress import track

from database import queries
from dependencies import get_connection, require_skip_nomenclatures_downloading
from exceptions import WarehousesDoNotExistError
from helpers import chunkify, count_chunks
from models import WarehouseStocksRow
from parsers.http_responses import (
    parse_warehouses_response,
    parse_stocks_response,
)
from parsers.workbooks.stocks import parse_stocks_workbook
from services.connection import WildberriesAPIConnection
from services.nomenclatures import download_all_nomenclatures
from services.workbook import closing_workbook


def iter_all_skus(
        *,
        limit: int = 1000,
        offset: int = 0,
) -> Generator[list[str], None, None]:
    while True:
        skus = queries.get_skus(limit=limit, offset=offset)
        if skus:
            yield skus
        else:
            break
        offset += limit


def iter_all_stocks(
        *,
        limit: int = 1000,
        offset: int = 0,
) -> Generator[list[WarehouseStocksRow], None, None]:
    while True:
        nomenclatures_stocks = queries.get_stocks(limit=limit, offset=offset)
        if nomenclatures_stocks:
            yield nomenclatures_stocks
        else:
            break
        offset += limit


@inject
def download(
        file_path: pathlib.Path,
        console: Console = Depends(get_console),
        connection: WildberriesAPIConnection = Depends(get_connection),
        skip_nomenclatures_downloading: bool = Depends(
            require_skip_nomenclatures_downloading,
        ),
) -> None:
    if not skip_nomenclatures_downloading:
        download_all_nomenclatures(connection=connection)

    warehouses_response = connection.get_warehouses()
    warehouses = parse_warehouses_response(warehouses_response)

    if not warehouses:
        raise WarehousesDoNotExistError

    loaded_stocks_count: int = 0
    for skus in iter_all_skus():
        for warehouse in warehouses:
            stocks_response = connection.get_stocks_by_skus(
                warehouse_id=warehouse.id,
                skus=skus,
            )
            stocks = parse_stocks_response(stocks_response)

            queries.add_sku_stocks(warehouse.id, stocks)

            loaded_stocks_count += len(stocks)

            console.log(f'Загружено {loaded_stocks_count} остатков')

    workbook = Workbook(write_only=True)
    headers = ('ID склада', 'sku', 'Количество остатков')

    console.log('Сохранение остатков в файл...')

    with contextlib.closing(workbook) as workbook:
        workbook: Workbook
        worksheet = workbook.create_sheet('Остатки')
        worksheet.append(headers)

        for warehouse_stocks in iter_all_stocks():

            for warehouse_stock in warehouse_stocks:
                worksheet.append((
                    warehouse_stock.warehouse_id,
                    warehouse_stock.sku,
                    warehouse_stock.stocks_amount,
                ))

    workbook.save(file_path)

    console.log('Остатки сохранены в файл')


@inject
def upload(
        file_path: pathlib.Path,
        console: Console = Depends(get_console),
        connection: WildberriesAPIConnection = Depends(get_connection),
) -> None:
    console.log('Чтение остатков из файла...')
    with closing_workbook(file_path) as workbook:
        warehouses_stocks = parse_stocks_workbook(workbook)
        console.log('Остатки загружены из файла')

    for warehouse_stocks in warehouses_stocks:
        chunks_iterator = chunkify(
            items=warehouse_stocks.stocks,
            chunk_size=1000,
        )

        stocks_count = len(warehouse_stocks.stocks)
        loaded_stocks_count: int = 0

        console.log(
            'Загрузка остатков в склад'
            f' №{warehouse_stocks.warehouse_id}...'
        )

        for stocks_chunk in chunks_iterator:
            connection.update_stocks(
                warehouse_id=warehouse_stocks.warehouse_id,
                stocks=stocks_chunk,
            )
            loaded_stocks_count += len(stocks_chunk)
            console.log(
                f'[{loaded_stocks_count}/{stocks_count}]'
                ' Загрузка остатков...'
            )

    console.log('Все остатки загружены')
