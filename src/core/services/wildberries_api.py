import logging
from typing import Iterable

import httpx
from pydantic import parse_obj_as

from core import exceptions, models

__all__ = ('WildberriesAPIService',)


class WildberriesAPIService:

    def __init__(self, api_client: httpx.Client):
        self.__api_client = api_client

    def update_stocks(self, warehouse_id: int, stocks: Iterable[models.StockToUpdate]):
        url = f'/api/v3/stocks/{warehouse_id}'
        request_data = {'stocks': [{'sku': stock.sku, 'amount': stock.amount} for stock in stocks]}
        response = self.__api_client.put(url, json=request_data)
        if response.is_success:
            return
        status_code_to_exception_class = {
            400: exceptions.BadRequestError,
            401: exceptions.UnauthorizedError,
            403: exceptions.PermissionDeniedError,
            404: exceptions.NotFoundError,
            409: exceptions.StocksUpdateError,
        }
        exception_class = status_code_to_exception_class.get(response.status_code, exceptions.BadRequestError)
        raise exception_class(response=response)

    def get_prices(self, quantity_status: models.QuantityStatus) -> tuple[models.NomenclaturePrice, ...]:
        request_query_params = {'quantity': quantity_status.value}
        response = self.__api_client.get('/public/api/v1/info', params=request_query_params)
        if response.status_code == 401:
            raise exceptions.UnauthorizedError
        response_data = response.json()
        return parse_obj_as(tuple[models.NomenclaturePrice, ...], response_data)

    def update_prices(self, nomenclature_prices: Iterable[models.NomenclaturePriceToUpdate]) -> bool:
        request_data = [{'nmId': nomenclature_price.nomenclature_id, 'price': nomenclature_price.price}
                        for nomenclature_price in nomenclature_prices]
        response = self.__api_client.post('/public/api/v1/prices', json=request_data)
        logging.info(response.text)
        return response.is_success
