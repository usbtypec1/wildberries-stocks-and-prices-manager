from collections.abc import Iterable

from fast_depends import Depends, inject
from sqlalchemy import update, select, func
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

from database import models as db_models
from database.session_factory import get_session
from models import Nomenclature, NomenclaturePrice, StocksBySku


@inject
def add_nomenclatures(
        nomenclatures: Iterable[Nomenclature],
        session: Session = Depends(get_session, use_cache=False),
):
    nomenclatures = tuple(nomenclatures)
    values: list[dict] = [
        {
            'id': nomenclature.id,
            'subject_name': nomenclature.subject_name,
        }
        for nomenclature in nomenclatures
    ]

    session.execute(
        insert(db_models.Nomenclature)
        .on_conflict_do_nothing(index_elements=('id',)),
        values,
    )
    session.commit()

    values: list[dict] = []
    for nomenclature in nomenclatures:
        for sku in nomenclature.skus:
            values.append(
                {
                    'nomenclature_id': nomenclature.id,
                    'sku': sku,
                }
            )
    session.execute(
        insert(db_models.NomenclatureSku)
        .on_conflict_do_nothing(index_elements=('nomenclature_id', 'sku')),
        values,
    )
    session.commit()


@inject
def add_sku_stocks(
        warehouse_id: int,
        stocks: Iterable[StocksBySku],
        session: Session = Depends(get_session, use_cache=False),
):
    values: list[dict] = [
        {
            'warehouse_id': warehouse_id,
            'amount': stock.amount,
            'sku': stock.sku,
        }
        for stock in stocks
    ]

    statement = insert(db_models.SkuStocks).values(values)
    statement = statement.on_conflict_do_update(
        index_elements=['warehouse_id', 'sku'],
        set_={'amount': statement.excluded.amount},
    )
    session.execute(statement)

    session.commit()


@inject
def add_nomenclature_prices(
        nomenclature_prices: Iterable[NomenclaturePrice],
        session: Session = Depends(get_session, use_cache=False),
):
    statement = select(db_models.Nomenclature.id)
    result = session.execute(statement)
    nomenclature_ids = {row[0] for row in result.all()}

    values: list[dict] = [
        {
            'id': nomenclature_price.nomenclature_id,
            'price': nomenclature_price.price,
            'discount': nomenclature_price.discount,
        }
        for nomenclature_price in nomenclature_prices
        if nomenclature_price.nomenclature_id in nomenclature_ids
    ]

    session.execute(
        update(db_models.Nomenclature),
        values,
    )
    session.commit()


@inject
def get_skus(
        limit: int,
        offset: int,
        session: Session = Depends(get_session, use_cache=False),
) -> list[str]:
    statement = (
        select(db_models.NomenclatureSku.sku)
        .limit(limit)
        .offset(offset)
    )
    result = session.execute(statement)
    return [row[0] for row in result.all()]


@inject
def count_nomenclatures(
        session: Session = Depends(get_session, use_cache=False),
) -> int:
    statement = select(func.count(db_models.Nomenclature))
    result = session.execute(statement)
    return result.first()[0]


@inject
def count_skus(
        session: Session = Depends(get_session, use_cache=False),
) -> int:
    statement = select(func.count(db_models.NomenclatureSku))
    result = session.execute(statement)
    return result.first()[0]
