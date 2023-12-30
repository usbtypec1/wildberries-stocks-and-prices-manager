import contextlib
import pathlib

from openpyxl.workbook import Workbook
from rich.progress import track

from core.exceptions import WarehousesDoNotExistError
from core.helpers import chunkify, count_chunks
from core.models import WarehouseStocks
from core.parsers.http_responses import (
    parse_warehouses_response,
    parse_stocks_response,
)
from core.parsers.workbooks.stocks import parse_stocks_workbook
from core.services.connection import WildberriesAPIConnection
from core.services.http_clients import closing_wildberries_http_client
from core.services.manager import ManagerService
from core.services.nomenclatures import (
    get_all_nomenclatures,
    collect_nomenclatures_skus,
)
from core.services.workbook import closing_workbook


class StocksManager(ManagerService):

    def download(self, file_path: pathlib.Path) -> None:
        with closing_wildberries_http_client() as http_client:
            connection = WildberriesAPIConnection(
                http_client=http_client,
                token=self._token,
            )

            nomenclatures = get_all_nomenclatures(
                connection=connection,
                console=self._console,
            )

            skus = collect_nomenclatures_skus(nomenclatures)

            chunks_count = count_chunks(items=skus, chunk_size=1000)
            chunks_iterator = chunkify(items=skus, chunk_size=1000)

            warehouses_response = connection.get_warehouses()
            warehouses = parse_warehouses_response(warehouses_response)

            if not warehouses:
                raise WarehousesDoNotExistError

            warehouses_stocks: list[WarehouseStocks] = []

            self._console.log('Загрузка остатков...')
            for skus_chunk in track(
                    sequence=chunks_iterator,
                    description='Загрузка остатков...',
                    console=self._console,
                    total=chunks_count,
            ):
                for warehouse in warehouses:
                    stocks_response = connection.get_stocks_by_skus(
                        warehouse_id=warehouse.id,
                        skus=skus_chunk,
                    )
                    stocks = parse_stocks_response(stocks_response)

                    warehouses_stocks.append(
                        WarehouseStocks(
                            warehouse_id=warehouse.id,
                            stocks=stocks,
                        ),
                    )

        workbook = Workbook(write_only=True)
        headers = ('ID склада', 'sku', 'Количество остатков')

        with contextlib.closing(workbook) as workbook:
            workbook: Workbook
            worksheet = workbook.create_sheet('Остатки')
            worksheet.append(headers)

            for warehouse_stocks in warehouses_stocks:
                for stock in warehouse_stocks.stocks:
                    worksheet.append((
                        warehouse_stocks.warehouse_id,
                        stock.sku,
                        stock.amount,
                    ))

            workbook.save(file_path)

    def upload(self, file_path: pathlib.Path) -> None:
        with closing_workbook(file_path) as workbook:
            self._console.log('Чтение остатков из файла...')
            warehouses_stocks = parse_stocks_workbook(workbook)
            self._console.log('Остатки загружены из файла')

        with closing_wildberries_http_client() as http_client:
            connection = WildberriesAPIConnection(
                http_client=http_client,
                token=self._token,
            )

            for warehouse_stocks in warehouses_stocks:
                chunks_iterator = chunkify(
                    items=warehouse_stocks.stocks,
                    chunk_size=1000,
                )
                chunks_count = count_chunks(
                    items=warehouse_stocks.stocks,
                    chunk_size=1000,
                )

                description = (
                    'Загрузка остатков в склад'
                    f' №{warehouse_stocks.warehouse_id}...'
                )

                for stocks_chunk in track(
                        sequence=chunks_iterator,
                        description=description,
                        console=self._console,
                        total=chunks_count,
                ):
                    connection.update_stocks(
                        warehouse_id=warehouse_stocks.warehouse_id,
                        stocks=stocks_chunk,
                    )
