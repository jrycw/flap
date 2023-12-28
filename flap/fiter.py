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
        """Using islice directly is easier than dispatching"""
        self._iter = islice(self._iter, n, None)
        return self

    def take(self, n):
        """Using islice directly is easier than dispatching"""
        self._iter = islice(self._iter, n)
        return self

    def enumerate(self):
        return self._dispatch_func(enumerate)

    def zip(self, other):
        def zipp(x, *, y):
            return zip(x, y)

        return self._dispatch_func(partial(zipp, y=other))

    def filter(self, func):
        return self._dispatch_func(partial(filter, func))

    def map(self, func):
        return self._dispatch_func(partial(map, func))

    def _dispatch_func(self, func):
        self._iter = func(self._iter)
        return self


if __name__ == "__main__":
    start = time.perf_counter()
    f_iter = FIter(count())
    # f_iter = FIter(range(20))
    result = (
        f_iter.skip(1)
        .take(8_000_000)
        .skip(7_000_000)
        .enumerate()
        .zip("abcde")
        .filter(lambda x: x[-1] in "cd")
        .map(lambda x: x[0])
    )
    print(list(result))
    end = time.perf_counter()
    elapsed = time.perf_counter() - start
    print(f"elapsed: {elapsed:0.6f} secs")
