from typing import NewType

import httpx

__all__ = ('WildberriesHTTPClient',)

WildberriesHTTPClient = NewType('WildberriesHTTPClient', httpx.Client)
