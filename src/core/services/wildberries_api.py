import contextlib
import logging
from typing import Iterable, Generator

import httpx
from pydantic import parse_obj_as

import core.models.wildberries_api
from core import exceptions, models

__all__ = ('WildberriesAPIService',)


class WildberriesAPIService:

    def __init__(self, api_client: httpx.Client):
        self.__api_client = api_client

    def update_stocks(self, warehouse_id: int, stocks: Iterable[core.models.wildberries_api.StocksBySku]):
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

    def get_warehouses(self) -> tuple[models.Warehouse, ...]:
        url = '/api/v2/warehouses'
        response = self.__api_client.get(url)
        if response.status_code == 401:
            raise exceptions.UnauthorizedError(response=response)
        response_data = response.json()
        return parse_obj_as(tuple[models.Warehouse, ...], response_data)

    def get_stocks_by_skus(self, *, warehouse_id: int, skus: Iterable[str]) -> tuple[
        core.models.wildberries_api.StocksBySku, ...]:
        url = f'/api/v3/stocks/{warehouse_id}'
        request_data = {'skus': tuple(skus)}
        response = self.__api_client.post(url, json=request_data)
        response_data = response.json()
        return parse_obj_as(tuple[core.models.wildberries_api.StocksBySku, ...], response_data['stocks'])

    def get_nomenclatures(self) -> Generator[list[models.Nomenclature], None, None]:
        pagination_data = None
        while True:
            body = {
                "sort": {
                    "cursor": {
                        "limit": 1000,
                    },
                    "filter": {
                        "withPhoto": -1,
                    },
                },
            }
            if pagination_data is not None:
                body['sort']['cursor'] = body['sort']['cursor'] | pagination_data
            for _ in range(5):
                with contextlib.suppress(Exception):
                    response = self.__api_client.post('/content/v1/cards/cursor/list', json=body)
                    if response.is_error:
                        raise Exception
                    break
            data = response.json()['data']
            total = data['cursor']['total']
            yield parse_obj_as(list[models.Nomenclature], data['cards'])
            pagination_data = {'updatedAt': data['cursor']['updatedAt'], 'nmID': data['cursor']['nmID']}
            if total < 1000:
                break

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
