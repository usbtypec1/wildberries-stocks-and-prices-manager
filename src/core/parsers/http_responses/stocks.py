import httpx
from pydantic import TypeAdapter

from core.helpers.parsers import try_parse_response_json
from core.models import StocksBySku

__all__ = ('parse_stocks_response',)


def parse_stocks_response(response: httpx.Response) -> tuple[StocksBySku, ...]:
    response_data = try_parse_response_json(response)
    stocks = response_data['stocks']
    type_adapter = TypeAdapter(tuple[StocksBySku, ...])
    return type_adapter.validate_python(stocks)
