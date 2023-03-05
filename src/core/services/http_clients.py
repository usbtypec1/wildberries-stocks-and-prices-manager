import contextlib

import httpx

__all__ = ('closing_wildberries_api_http_client',)


@contextlib.contextmanager
def closing_wildberries_api_http_client(*, api_key: str, timeout=120) -> httpx.Client:
    base_url = 'https://suppliers-api.wildberries.ru/'
    headers = {'Authorization': f'Bearer {api_key}'}
    with httpx.Client(base_url=base_url, headers=headers, timeout=timeout) as client:
        yield client
