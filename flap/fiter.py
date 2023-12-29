from collections import deque  # noqa F401
from functools import partial, wraps
from itertools import count, islice  # noqa F401
import time


class FIter:
    stack = deque()

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
        self._consume_stack()
        return next(self._iter)

    def skip(self, n):
        def _islice(iterable, *, start, stop, step):
            return islice(iterable, start, stop, step)

        self.stack.append(partial(_islice, start=n, stop=None, step=1))
        return self

    def take(self, n):
        def _islice(iterable, *, start):
            return islice(iterable, start)

        self.stack.append(partial(_islice, start=n))
        return self

    def enumerate(self):
        self.stack.append(enumerate)
        return self

    def zip(self, other):
        def zipp(x, *, y):
            return zip(x, y)

        self.stack.append(partial(zipp, y=other))
        return self

    def filter(self, func):
        self.stack.append(partial(filter, func))
        return self

    def map(self, func):
        self.stack.append(partial(map, func))
        return self

    def _consume_stack(self):
        while self.stack:
            action = self.stack.popleft()
            self._iter = action(self._iter)

    def collect(self, constructor=list):
        self._consume_stack()
        return constructor(self._iter)


def timer(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"elapsed: {elapsed:0.6f} secs")
        return result

    return wrapper


@timer
def compute(lazy_iter):
    return lazy_iter.collect()


if __name__ == "__main__":
    f_iter = FIter(count())
    # f_iter = FIter(range(20))

    lazy_iter = (
        f_iter.skip(1)
        .take(8_000_000)
        .skip(8_000_000)
        .enumerate()
        .zip("abcde")
        .filter(lambda x: x[-1] in "cd")
        .map(lambda x: x[0])
    )

    compute(lazy_iter)
