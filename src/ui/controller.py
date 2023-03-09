import collections
import os.path
import sys
from typing import Any, DefaultDict

import PySimpleGUI as sg
from openpyxl.utils.exceptions import InvalidFileException
from rich.console import Console
from rich.live import Live
from rich.progress import track
from rich.table import Table

import core.models
from core import exceptions, models
from core.helpers import grouper
from core.services.http_clients import closing_wildberries_api_http_client
from core.services.wildberries_api import WildberriesAPIService
from core.shortcuts import run
from core.templates import Template
from core.validators import validate_api_key


def handle_event(window: sg.Window, event: Any, values: Any) -> None:
    match event:
        case '-GENERATE-TEMPLATE-FILE-':
            file_path = os.path.join(os.path.dirname(sys.executable), 'шаблон.xlsx')
            print(file_path)
            with Template(file_path) as template:
                template.save()
                sg.popup(f'Шаблон сохранен в {str(file_path)}')

        case '-DOWNLOAD-STOCKS-':
            api_key: str | None = values.get('-API-KEY-INPUT-')
            try:
                validate_api_key(api_key)
            except exceptions.ValidationError as error:
                sg.popup(str(error))
                return

            sg.popup('Сейчас пойдет загрузка остатков. Процесс займет от 3 до 15 минут...', custom_text='Начать')
            download_stocks(api_key)
            sg.popup('Остатки выгружены')

        case '-DOWNLOAD-PRICES-':
            api_key: str | None = values.get('-API-KEY-INPUT-')
            try:
                validate_api_key(api_key)
            except exceptions.ValidationError as error:
                sg.popup(str(error))
                return

            try:
                download_prices(api_key)
            except exceptions.UnauthorizedError:
                sg.popup_error('Неправильный API ключ')

        case '-START-':
            window['LOGS'].update(visible=True)
            api_key: str | None = values.get('-API-KEY-INPUT-')
            try:
                validate_api_key(api_key)
            except exceptions.ValidationError as error:
                sg.popup(str(error))
                return

            file_path = values.get('-FILE-')
            if not file_path:
                sg.popup('Выберите excel файл, который будете загружать')
                return

            window['-START-'].update(disabled=True)
            try:
                run(api_key, file_path)
            except exceptions.WorkbookValidationError as error:
                error_message = (f'Ошибка в строке в {error.row_number}, '
                                 f'на странице "{error.worksheet_name}"\n'
                                 f'{str(error).capitalize()}')
                sg.popup_error(error_message)
            except InvalidFileException:
                sg.popup_error('Выбранный файл не является excel файлом')
            else:
                sg.popup('Данные успешно обновлены')
            window['-START-'].update(disabled=False)


def download_stocks(console: Console, api_key: str):
    warehouse_id_to_stocks_by_skus: DefaultDict[int, list[
        core.models.wildberries_api.StocksBySku]] = collections.defaultdict(list)
    skus: set[str] = set()

    with closing_wildberries_api_http_client(api_key=api_key) as http_client:
        wildberries_api_service = WildberriesAPIService(http_client)

        warehouses = wildberries_api_service.get_warehouses()
        console.log('Информация о складах загружена')
        for nomenclatures in track(
                sequence=wildberries_api_service.get_nomenclatures(),
                description='Загрузка всех skus...',
                console=console,
        ):
            skus |= {
                sku
                for nomenclature in nomenclatures
                for size in nomenclature['sizes']
                for sku in size['skus']
                if sku
            }

        for skus_group in track(
                sequence=grouper(skus, n=1000),
                description='Загрузка остатков по skus',
                console=console,
        ):
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
    console.log('Остатки выгружены')


def download_prices(console: Console, api_key: str):
    with closing_wildberries_api_http_client(api_key=api_key) as http_client:
        wildberries_api_service = WildberriesAPIService(http_client)
        with console.status('Загрузка цен...', spinner='bouncingBall'):
            nomenclature_prices = wildberries_api_service.get_prices(models.QuantityStatus.ANY)

    with Template('./выгрузка цен.xlsx') as template:
        template.add_prices_rows(nomenclature_prices)
    console.log('Цены выгружены')
