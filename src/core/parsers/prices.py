import httpx
from pydantic import TypeAdapter

from core.helpers.parsers import try_parse_response_json
from core.models import NomenclaturePrice

__all__ = ('parse_prices_response',)


def parse_prices_response(
        response: httpx.Response,
) -> tuple[NomenclaturePrice, ...]:
    response_data = try_parse_response_json(response)
    type_adapter = TypeAdapter(tuple[NomenclaturePrice, ...])
    return type_adapter.validate_python(response_data)
