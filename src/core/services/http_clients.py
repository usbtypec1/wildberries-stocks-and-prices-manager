import contextlib

import httpx

from core.models.http_clients import WildberriesHTTPClient

__all__ = ('closing_wildberries_http_client',)


@contextlib.contextmanager
def closing_wildberries_http_client(
        *,
        timeout: int = 120,
) -> WildberriesHTTPClient:
    base_url = 'https://suppliers-api.wildberries.ru/'
    with httpx.Client(
            base_url=base_url,
            timeout=timeout,
    ) as http_client:
        yield WildberriesHTTPClient(http_client)
