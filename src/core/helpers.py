from itertools import zip_longest

__all__ = ('grouper',)


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return ([i for i in group if i is not None] for group in zip_longest(*args, fillvalue=fillvalue))
