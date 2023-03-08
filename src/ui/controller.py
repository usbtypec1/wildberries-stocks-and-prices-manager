import contextlib
import pathlib

import PySimpleGUI as sg

from typing import Any

from openpyxl.utils.exceptions import InvalidFileException

from core import exceptions
from core.shortcuts import download_prices, run, download_stocks
from core.templates import Template
from core.validators import validate_api_key


def handle_event(window: sg.Window, event: Any, values: Any) -> None:
    match event:
        case '-GENERATE-TEMPLATE-FILE-':
            with Template(pathlib.Path(__file__).parent / 'шаблон.xlsx') as template:
                template.save()

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
