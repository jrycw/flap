from collections import deque  # noqa F401
from functools import partial
from itertools import count, islice  # noqa F401
import time


class FIter:
    def __init__(self, iterable):
        self._iter = iter(iterable)

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

    def skip(self, n):
        self._iter = iter(islice(self._iter, n, None))
        return self

    def take(self, n):
        self._iter = iter(islice(self._iter, n))
        return self

    def enumerate(self):
        """slow"""
        return self._dispatch_func(enumerate)

    def zip(self, other):
        return self._dispatch_func(zip, other)

    def filter(self, func):
        return self._dispatch_func(partial(filter, func))

    def map(self, func):
        return self._dispatch_func(partial(map, func))

    def _dispatch_func(self, func, other=None):
        if other is None:
            self._iter = iter(func(self._iter))
        else:
            self._iter = iter(func(self._iter, other))
        return self


if __name__ == "__main__":
    start = time.perf_counter()
    f_iter = FIter(count())
    # f_iter = FIter(range(20))
    result = (
        f_iter.skip(1)
        .skip(2)
        .skip(3)
        .take(8_000_000)
        .skip(7_000_000)
        .enumerate()
        .zip("abcde")
        .filter(lambda x: x[-1] in "cd")
        .map(lambda x: x[0])
    )
    print(f"{type(result)=}, {result=}, {list(result)=}")
    end = time.perf_counter()
    print(end - start)
