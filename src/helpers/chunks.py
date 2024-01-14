from collections.abc import Iterable

from typing import TypeVar, Generator, Any

__all__ = ('chunkify', 'count_chunks')

T = TypeVar('T')


def chunkify(
        *,
        items: Iterable[T],
        chunk_size: int,
) -> Generator[list[T], None, None]:
    items = tuple(items)
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]


def count_chunks(
        *,
        items: Iterable[Any],
        chunk_size: int,
) -> int:
    items = tuple(items)
    items_count = len(items)
    return items_count // chunk_size + ((items_count % chunk_size) > 0)
