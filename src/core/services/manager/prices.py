import contextlib
import pathlib
import time

from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from rich import progress

from core.enums import QuantityStatus
from core.helpers import chunkify
from core.parsers.http_responses import parse_prices_response
from core.parsers.workbooks.prices import parse_prices_workbook
from core.services.connection import WildberriesAPIConnection
from core.services.http_clients import closing_wildberries_http_client
from core.services.manager.base import ManagerService
from core.services.nomenclatures import (
    merge_nomenclatures_and_prices,
    get_all_nomenclatures
)
from core.services.workbook import closing_workbook


class PricesManager(ManagerService):

    def download(self, destination_path: pathlib.Path) -> None:
        with closing_wildberries_http_client() as http_client:
            connection = WildberriesAPIConnection(
                http_client=http_client,
                token=self._token,
            )

            self._console.log('Загрузка цен...')
            prices_response = connection.get_prices(QuantityStatus.ANY)
            self._console.log('Цены загружены')

            prices = parse_prices_response(prices_response)

            nomenclatures = get_all_nomenclatures(
                connection=connection,
                console=self._console,
            )

        nomenclatures_with_prices = merge_nomenclatures_and_prices(
            nomenclatures=nomenclatures,
            prices=prices,
        )

        workbook = Workbook(write_only=True)
        headers = ('Категория товара', 'nm ID', 'Новая цена', 'Скидка')
        with contextlib.closing(workbook) as workbook:
            workbook: Workbook
            worksheet: Worksheet = workbook.create_sheet('Цены')
            worksheet.append(headers)

            for nomenclature in nomenclatures_with_prices:
                worksheet.append((
                    nomenclature.subject_name,
                    nomenclature.id,
                    nomenclature.price,
                    nomenclature.discount,
                ))

            workbook.save(destination_path)

    def upload(self, file_path: pathlib.Path) -> None:
        with closing_workbook(file_path) as workbook:
            nomenclature_prices = parse_prices_workbook(workbook)

        nomenclature_prices_chunks = chunkify(
            items=nomenclature_prices,
            chunk_size=1000,
        )

        with closing_wildberries_http_client() as http_client:
            connection = WildberriesAPIConnection(
                http_client=http_client,
                token=self._token,
            )

            for nomenclature_prices_chunk in progress.track(
                    nomenclature_prices_chunks,
                    description='Загрузка цен...',
                    console=self._console,
            ):
                time.sleep(0.1)
                connection.update_prices(
                    nomenclature_prices=nomenclature_prices_chunk
                )
