from typing import Iterable

import httpx

import models

__all__ = ('WildberriesAPIService',)


class WildberriesAPIService:

    def __init__(self, api_client: httpx.Client):
        self.__api_client = api_client

    def update_stocks(self, warehouse_id: int, stocks: Iterable[models.StockToUpdate]) -> bool:
        url = f'/api/v3/stocks/{warehouse_id}'
        request_data = {'stocks': [stock.dict() for stock in stocks]}
        response = self.__api_client.put(url, json=request_data)
        return response.is_success
