import httpx
from pydantic import TypeAdapter

from core.helpers.parsers import try_parse_response_json
from core.models import Nomenclature

__all__ = ('parse_nomenclatures_response',)


def parse_nomenclatures_response(
        response: httpx.Response,
) -> tuple[Nomenclature, ...]:
    response_data = try_parse_response_json(response)
    cards = response_data['cards']
    type_adapter = TypeAdapter(tuple[Nomenclature, ...])
    return type_adapter.validate_python(cards)
