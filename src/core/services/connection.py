from collections.abc import Iterable, Generator
from functools import cached_property

import httpx

from core.enums import QuantityStatus
from core.helpers.http import handle_error_status_code
from core.helpers.parsers import try_parse_response_json
from core.models import (
    StocksBySku,
    NomenclaturePriceToUpdate,
    WildberriesHTTPClient,
)

__all__ = ('WildberriesAPIConnection',)


class WildberriesAPIConnection:
    """
    Provides connection to Wildberries API methods.
    Each method represents API call on the Wildberries side
    and returns httpx.Response.
    In case of error (based on status code) raises corresponding exception.
    """

    def __init__(
            self,
            http_client: WildberriesHTTPClient,
            token: str,
    ):
        self.__http_client = http_client
        self.__token = token

    @cached_property
    def headers(self) -> dict[str, str]:
        return {'Authorization': f'Bearer {self.__token}'}

    def update_stocks(
            self,
            *,
            warehouse_id: int,
            stocks: Iterable[StocksBySku],
    ):
        url = f'/api/v3/stocks/{warehouse_id}'
        request_data = {
            'stocks': [
                {
                    'sku': stock.sku,
                    'amount': stock.amount,
                } for stock in stocks
            ]
        }
        response = self.__http_client.put(
            url=url,
            json=request_data,
            headers=self.headers,
        )
        handle_error_status_code(response)
        return response

    def get_warehouses(self) -> httpx.Response:
        url = '/api/v3/warehouses'
        response = self.__http_client.get(
            url=url,
            headers=self.headers,
        )
        handle_error_status_code(response)
        return response

    def get_stocks_by_skus(
            self,
            *,
            warehouse_id: int,
            skus: Iterable[str],
    ) -> httpx.Response:
        url = f'/api/v3/stocks/{warehouse_id}'
        request_data = {'skus': tuple(skus)}
        response = self.__http_client.post(
            url=url,
            json=request_data,
            headers=self.headers,
        )
        handle_error_status_code(response)
        return response

    def iter_nomenclatures(self) -> Generator[httpx.Response, bool, None]:
        pagination_data = None
        url = '/content/v2/get/cards/list'

        while True:
            body = {
                'settings': {
                    'cursor': {'limit': 1000},
                    'filter': {'withPhoto': -1},
                },
            }
            if pagination_data is not None:
                body['settings']['cursor'] = {'limit': 1000} | pagination_data

            response = self.__http_client.post(
                url=url,
                json=body,
                headers=self.headers,
            )

            handle_error_status_code(response)
            should_repeat = yield response

            if not should_repeat:
                response_data = try_parse_response_json(response)

                pagination_data = {
                    'updatedAt': response_data['cursor']['updatedAt'],
                    'nmID': response_data['cursor']['nmID']
                }

                if response_data['cursor']['total'] < 1000:
                    break

    def get_prices(self, quantity_status: QuantityStatus) -> httpx.Response:
        request_query_params = {'quantity': quantity_status.value}
        url = '/public/api/v1/info'
        response = self.__http_client.get(
            url=url,
            params=request_query_params,
            headers=self.headers,
        )
        handle_error_status_code(response)
        return response

    def update_prices(
            self,
            nomenclature_prices: Iterable[NomenclaturePriceToUpdate],
    ) -> httpx.Response:
        request_data = [
            {
                'nmId': nomenclature_price.nomenclature_id,
                'price': nomenclature_price.price
            } for nomenclature_price in nomenclature_prices
        ]
        url = '/public/api/v1/prices'
        response = self.__http_client.post(
            url=url,
            json=request_data,
            headers=self.headers,
        )
        handle_error_status_code(response)
        return response
