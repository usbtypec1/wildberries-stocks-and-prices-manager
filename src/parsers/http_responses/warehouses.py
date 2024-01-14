import httpx
from pydantic import TypeAdapter

from helpers.parsers import try_parse_response_json
from models import Warehouse

__all__ = ('parse_warehouses_response',)


def parse_warehouses_response(
        response: httpx.Response,
) -> tuple[Warehouse, ...]:
    response_data = try_parse_response_json(response)
    type_adapter = TypeAdapter(tuple[Warehouse, ...])
    return type_adapter.validate_python(response_data)
