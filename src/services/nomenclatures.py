from collections.abc import Iterable

from fast_depends import Depends, inject
from rich import get_console
from rich.console import Console
from rich.progress import track

from database.queries import add_nomenclatures
from exceptions import WildberriesAPIError
from models import Nomenclature, NomenclaturePrice, NomenclatureWithPrice
from parsers.http_responses import parse_nomenclatures_response
from services.connection import WildberriesAPIConnection


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


@inject
def download_all_nomenclatures(
        connection: WildberriesAPIConnection,
        console: Console = Depends(get_console),
) -> None:
    nomenclatures_iterator = connection.iter_nomenclatures()

    console.log('Загрузка номенклатур...')
    downloaded_nomenclatures_count: int = 0

    for nomenclatures_response in nomenclatures_iterator:
        try:
            nomenclatures = parse_nomenclatures_response(
                response=nomenclatures_response,
            )
        except WildberriesAPIError:
            console.log(
                'Ошибка при загрузке цен. Пробуем ещё раз...',
            )
            nomenclatures_iterator.send(True)
        else:
            add_nomenclatures(nomenclatures)

            downloaded_nomenclatures_count += len(nomenclatures)
            console.log(
                f'Загружено {downloaded_nomenclatures_count} номенклатур',
            )

    console.log('✅ Номенклатуры загружены')
