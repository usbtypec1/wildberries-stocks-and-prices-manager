from sqlalchemy import create_engine, Engine

__all__ = ('get_engine',)


def get_engine() -> Engine:
    return create_engine(
        'sqlite:///../cache.db',
    )
