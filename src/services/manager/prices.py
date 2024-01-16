import contextlib
import pathlib
import time
from collections.abc import Generator

from fast_depends import Depends, inject
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from rich import progress, get_console
from rich.console import Console

from database import queries
from dependencies import get_connection, require_skip_nomenclatures_downloading
from enums import QuantityStatus
from helpers import chunkify
from models import NomenclaturePriceWithSubjectName
from parsers.http_responses import parse_prices_response
from parsers.workbooks.prices import parse_prices_workbook
from services.connection import WildberriesAPIConnection
from services.nomenclatures import download_all_nomenclatures
from services.workbook import closing_workbook


def iter_prices(
        *,
        limit: int = 1000,
        offset: int = 0,
) -> Generator[list[NomenclaturePriceWithSubjectName], None, None]:
    while True:
        prices = queries.get_prices(limit=limit, offset=offset)
        if prices:
            yield prices
        else:
            break
        offset += limit


@inject
def download(
        destination_path: pathlib.Path,
        console: Console = Depends(get_console),
        connection: WildberriesAPIConnection = Depends(get_connection),
        skip_nomenclatures_downloading: bool = Depends(
            require_skip_nomenclatures_downloading,
        ),
) -> None:
    if not skip_nomenclatures_downloading:
        download_all_nomenclatures(connection=connection)

    console.log('Загрузка цен из API Wildberries...')
    prices_response = connection.get_prices(QuantityStatus.ANY)
    console.log('Цены из API Wildberries загружены')

    prices = parse_prices_response(prices_response)

    queries.add_nomenclature_prices(prices)

    console.log('Сохранение цен в файл...')

    workbook = Workbook(write_only=True)

    headers = ('Категория товара', 'nm ID', 'Новая цена', 'Скидка')

    with contextlib.closing(workbook) as workbook:
        workbook: Workbook
        worksheet: Worksheet = workbook.create_sheet('Цены')
        worksheet.append(headers)

        for prices in iter_prices():
            for nomenclature_price in prices:
                worksheet.append((
                    nomenclature_price.subject_name,
                    nomenclature_price.nomenclature_id,
                    nomenclature_price.price,
                    nomenclature_price.discount,
                ))

    workbook.save(destination_path)

    console.log('Цены записаны в файл')


@inject
def upload(
        file_path: pathlib.Path,
        console: Console = Depends(get_console),
        connection: WildberriesAPIConnection = Depends(get_connection),
) -> None:
    with closing_workbook(file_path) as workbook:
        nomenclature_prices = parse_prices_workbook(workbook)

    nomenclature_prices_chunks = chunkify(
        items=nomenclature_prices,
        chunk_size=1000,
    )

    total_count = len(nomenclature_prices)
    loaded_count: int = 0

    for nomenclature_prices_chunk in nomenclature_prices_chunks:
        time.sleep(0.1)
        connection.update_prices(nomenclature_prices_chunk)
        loaded_count += len(nomenclature_prices_chunk)

        console.log(f'[{loaded_count}/{total_count}] Загрузка цен...')

    console.log('Цены загружены')
