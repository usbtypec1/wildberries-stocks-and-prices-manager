import contextlib

import httpx

from core.models.http_clients import WildberriesHTTPClient

__all__ = ('closing_wildberries_http_client',)


@contextlib.contextmanager
def closing_wildberries_http_client(
        *,
        api_key: str,
        timeout: int = 120,
) -> WildberriesHTTPClient:
    base_url = 'https://suppliers-api.wildberries.ru/'
    headers = {'Authorization': f'Bearer {api_key}'}
    with httpx.Client(
            base_url=base_url,
            headers=headers,
            timeout=timeout,
    ) as http_client:
        yield WildberriesHTTPClient(http_client)
