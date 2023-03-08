from core import exceptions


def validate_api_key(api_key: str) -> None:
    if not api_key or api_key == 'API ключ':
        raise exceptions.ValidationError('Введите API ключ')
    if not api_key.isascii():
        raise exceptions.ValidationError('Неправильный API ключ')
