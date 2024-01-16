from collections.abc import Iterable

from fast_depends import Depends, inject
from sqlalchemy import update, select, func
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

from database import models as db_models
from database.session_factory import get_session
from models import (
    Nomenclature, NomenclaturePrice, StocksBySku,
    WarehouseStocksRow, NomenclaturePriceWithSubjectName
)


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

    statement = insert(db_models.SkuStock).values(values)
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


@inject
def get_stocks(
        limit: int = 1000,
        offset: int = 0,
        session: Session = Depends(get_session, use_cache=False),
):
    statement = (
        select(
            db_models.NomenclatureSku.sku,
            db_models.SkuStock.warehouse_id,
            db_models.SkuStock.amount,
        )
        .join(
            db_models.NomenclatureSku,
            onclause=db_models.SkuStock.sku == db_models.NomenclatureSku.sku
        )
        .join(
            db_models.Nomenclature,
            onclause=(
                    db_models.NomenclatureSku.nomenclature_id
                    == db_models.Nomenclature.id
            ),
        )
        .limit(limit)
        .offset(offset)
    )
    result = session.execute(statement)
    return [
        WarehouseStocksRow(
            sku=sku,
            warehouse_id=warehouse_id,
            stocks_amount=amount,
        )
        for sku, warehouse_id, amount in result.all()
    ]


@inject
def get_prices(
        limit: int = 1000,
        offset: int = 0,
        session: Session = Depends(get_session, use_cache=False),
) -> list:
    statement = (
        select(
            db_models.Nomenclature.id,
            db_models.Nomenclature.subject_name,
            db_models.Nomenclature.price,
            db_models.Nomenclature.discount,
        )
        .limit(limit)
        .offset(offset)
    )
    result = session.execute(statement)
    return [
        NomenclaturePriceWithSubjectName(
            nomenclature_id=nomenclature_id,
            subject_name=subject_name,
            price=price,
            discount=discount,
        )
        for nomenclature_id, subject_name, price, discount in result.all()
    ]
