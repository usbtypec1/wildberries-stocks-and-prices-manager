from fast_depends import Depends
from rich import get_console
from rich.console import Console
from rich.prompt import Prompt

from models import WildberriesHTTPClient
from services.api_keys import require_api_key
from services.connection import WildberriesAPIConnection
from services.http_clients import get_http_client

__all__ = ('get_connection', 'require_skip_nomenclatures_downloading')


def get_connection(
        token: str = Depends(require_api_key),
        http_client: WildberriesHTTPClient = Depends(get_http_client),
) -> WildberriesAPIConnection:
    yield WildberriesAPIConnection(
        http_client=http_client,
        token=token,
    )


def require_skip_nomenclatures_downloading(
        console: Console = Depends(get_console),
) -> bool:
    choices = ['да', 'нет']
    while True:
        choice = Prompt.ask(
            prompt='Пропустить загрузку номенклатур?',
            console=console,
            choices=choices,
            default='нет',
        )
        if choice == 'да':
            return True
        if choice == 'нет':
            return False
