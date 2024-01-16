from fast_depends import Depends, inject
from rich import get_console
from rich.console import Console
from rich.prompt import Prompt

from exceptions import ValidationError
from validators import validate_api_key

__all__ = ('require_api_key',)


@inject
def require_api_key(console: Console = Depends(get_console)) -> str:
    while True:
        api_key = Prompt.ask('Введите API ключ')
        try:
            validate_api_key(api_key)
        except ValidationError:
            console.print('Неправильный API ключ')
        else:
            return api_key
