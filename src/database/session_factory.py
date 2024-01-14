from fast_depends import Depends
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, Session

from database.engine import get_engine

__all__ = ('get_session',)


def get_session(
        engine: Engine = Depends(get_engine),
) -> Session:
    session_maker = sessionmaker(bind=engine)
    with session_maker() as session:
        yield session
