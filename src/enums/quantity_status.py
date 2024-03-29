from enum import IntEnum

__all__ = ('QuantityStatus',)


class QuantityStatus(IntEnum):
    ANY = 0
    ONLY_WITH_STOCKS = 1
