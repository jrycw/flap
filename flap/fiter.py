from collections import deque  # noqa F401
from functools import partial
from itertools import count, islice  # noqa F401


class IteratorExhaustedError(Exception):
    """Iterator is exhausted"""


class FIter:
    def __init__(self, iterable):
        self._iter = (item for item in iterable)

    def __iter__(self):
        return self

    def __next__(self):
        """
        try:
            return next(self._iter)
        except StopIteration:
            raise
        """
        return next(self._iter)

    def _get_next(self):
        try:
            return next(self)  # or next(self._iter)
        except StopIteration:
            raise IteratorExhaustedError("Iterator is exhausted")

    def skip(self, n):
        for _ in range(n):
            self._get_next()
        return self

    def take(self, n):
        try:
            self._iter = (item for item in islice(self._iter, n))
        except StopIteration:
            raise IteratorExhaustedError("Iterator is exhausted")
        else:
            return self

    def enumerate(self):
        return self._dispatch_func(enumerate)

    def zip(self, other):
        return self._dispatch_func(zip, other)

    def filter(self, func):
        return self._dispatch_func(partial(filter, func))

    def map(self, func):
        return self._dispatch_func(partial(map, func))

    def _dispatch_func(self, func, other=None):
        if other is None:
            self._iter = (item for item in func(self._iter))
        else:
            self._iter = (item for item in func(self._iter, other))
        return self


if __name__ == "__main__":
    f_iter = FIter(count())
    # f_iter = FIter(range(20))
    result = (
        f_iter.skip(1)
        .skip(2)
        .skip(3)
        .take(8)
        .skip(4)
        .enumerate()
        .zip("abcde")
        .filter(lambda x: x[-1] in "cd")
        .map(lambda x: x[0])
    )
    print(f"{type(result)=}, {result=}, {list(result)=}")
