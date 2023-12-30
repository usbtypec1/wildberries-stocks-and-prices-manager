import pathlib

from rich.console import Console
from rich.prompt import Prompt, Confirm

from core import exceptions
from core.services.manager import StocksManager
from core.services.manager.prices import PricesManager
from core.templates import generate_template_file
from core.validators import validate_api_key


def terminate(console: Console):
    Prompt.ask('Goodbye', console=console)
    exit(0)


def require_api_key(console: Console) -> str:
    while True:
        api_key = Prompt.ask('Введите API ключ')
        try:
            validate_api_key(api_key)
        except exceptions.ValidationError:
            console.print('Неправильный API ключ')
        else:
            return api_key


def require_file_not_exists(console: Console, file_path: pathlib.Path):
    if file_path.exists():
        text = 'Шаблон уже присутствует в директории. Заменить?'
        is_replace_template_confirmed = Confirm.ask(text)
        if not is_replace_template_confirmed:
            terminate(console)


def require_file(console: Console, file_path: pathlib.Path):
    if not file_path.exists():
        text = (
            'Отсутствует файл'
            f' [b][u]{file_path.name}[/u][/b]'
            ' в текущей директории'
        )
        console.print(text)
        terminate(console)


def run(console: Console):
    action_number = Prompt.ask(
        prompt=(
            'Выберите действие'
            '\n1 - Загрузить остатки'
            '\n2 - Загрузить цены'
            '\n3 - Выгрузить все остатки'
            '\n4 - Выгрузить все цены'
            '\n5 - Сгенерировать шаблон'
            '\n0 - Выход\n'
        ),
        choices=['1', '2', '3', '4', '5', '0'],
    )
    match int(action_number):
        case 0:
            terminate(console)
        case 1:
            file_path = pathlib.Path('./остатки.xlsx')
            require_file(console, file_path)
            api_key = require_api_key(console)
            stocks_manager = StocksManager(console, api_key)
            stocks_manager.upload(file_path)
        case 2:
            file_path = pathlib.Path('./цены.xlsx')
            require_file(console, file_path)
            api_key = require_api_key(console)
            prices_manager = PricesManager(console, api_key)
            prices_manager.upload(file_path)
        case 3:
            file_path = pathlib.Path('./выгрузка остатков.xlsx')
            require_file_not_exists(console, file_path)
            api_key = require_api_key(console)
            stocks_manager = StocksManager(console, api_key)
            stocks_manager.download(file_path)
        case 4:
            file_path = pathlib.Path('./выгрузка цен.xlsx')
            require_file_not_exists(console, file_path)
            api_key = require_api_key(console)
            service = PricesManager(console, api_key)
            service.download(file_path)
        case 5:
            file_path = pathlib.Path('./шаблон.xlsx')
            require_file_not_exists(console, file_path)
            generate_template_file(file_path)
            console.log('Шаблон сохранен')

    terminate(console)
