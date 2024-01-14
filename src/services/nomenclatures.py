from collections.abc import Iterable

from rich.console import Console
from rich.progress import track

from exceptions import WildberriesAPIError
from models import Nomenclature, NomenclaturePrice, NomenclatureWithPrice
from parsers.http_responses import parse_nomenclatures_response
from services.connection import WildberriesAPIConnection


def collect_nomenclature_skus(nomenclature: Nomenclature) -> set[str]:
    return {
        sku
        for size in nomenclature.sizes
        for sku in size.skus
        if sku
    }


def collect_nomenclatures_skus(
        nomenclatures: Iterable[Nomenclature],
) -> set[str]:
    return {
        sku
        for nomenclature in nomenclatures
        for sku in collect_nomenclature_skus(nomenclature)
    }


def merge_nomenclatures_and_prices(
        nomenclatures: Iterable[Nomenclature],
        prices: Iterable[NomenclaturePrice],
) -> list[NomenclatureWithPrice]:
    nomenclature_id_to_price = {
        nomenclature_price.nomenclature_id: nomenclature_price
        for nomenclature_price in prices
    }

    nomenclatures_with_prices: list[NomenclatureWithPrice] = []
    for nomenclature in nomenclatures:
        try:
            nomenclature_price = nomenclature_id_to_price[nomenclature.id]
        except KeyError:
            continue
        nomenclatures_with_prices.append(
            NomenclatureWithPrice(
                **nomenclature.model_dump(),
                price=nomenclature_price.price,
                discount=nomenclature_price.discount,
                promocode=nomenclature_price.promocode,
            ),
        )

    return nomenclatures_with_prices


def get_all_nomenclatures(
        connection: WildberriesAPIConnection,
        console: Console,
) -> list[Nomenclature]:
    nomenclatures_iterator = connection.iter_nomenclatures()

    console.log('Загрузка номенклатур...')
    nomenclatures: list[Nomenclature] = []
    for nomenclatures_response in track(
            nomenclatures_iterator,
            description='Загрузка номенклатур',
            console=console,
    ):
        try:
            nomenclatures += parse_nomenclatures_response(
                response=nomenclatures_response,
            )
        except WildberriesAPIError:
            console.log(
                'Ошибка при загрузке цен. Пробуем ещё раз...',
            )
            nomenclatures_iterator.send(True)

    return nomenclatures
