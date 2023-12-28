from collections.abc import Iterable

from typing import TypeVar, Generator

__all__ = ('chunkify',)

T = TypeVar('T')


def chunkify(
        *,
        items: Iterable[T],
        chunk_size: int,
) -> Generator[list[T], None, None]:
    items = tuple(items)
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]
