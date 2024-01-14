from fast_depends import Depends, inject
from sqlalchemy import Engine
from sqlalchemy.orm import DeclarativeBase

from database.engine import get_engine

__all__ = ('Base', 'create_tables')


class Base(DeclarativeBase):
    __abstract__ = True


@inject
def create_tables(engine: Engine = Depends(get_engine)) -> None:
    Base.metadata.create_all(engine)
