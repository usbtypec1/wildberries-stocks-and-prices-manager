from core import exceptions
from core.services.http_clients import closing_wildberries_api_http_client
from core.services.wildberries_api import WildberriesAPIService


def validate_api_key(api_key: str) -> None:
    if not api_key or api_key == 'API ключ':
        raise exceptions.ValidationError('Введите API ключ')
    if not api_key.isascii():
        raise exceptions.ValidationError('Неправильный API ключ')
    # with closing_wildberries_api_http_client(api_key=api_key) as http_client:
    #     try:
    #         WildberriesAPIService(http_client).get_warehouses()
    #     except exceptions.UnauthorizedError:
    #         raise exceptions.ValidationError('Неправильный API ключ')
