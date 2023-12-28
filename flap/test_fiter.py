from itertools import count

import pytest

from .fiter import FIter, IteratorExhaustedError


@pytest.fixture
def f_iter():
    return FIter(count())


def test_skip(f_iter):
    lazy_iter = f_iter.skip(2)
    assert next(lazy_iter) == 2
    assert next(lazy_iter) == 3
    assert next(lazy_iter) == 4


def test_take(f_iter):
    lazy_iter = f_iter.take(2)
    assert list(lazy_iter) == [0, 1]


def test_map(f_iter):
    lazy_iter = f_iter.map(lambda x: x % 2)
    assert next(lazy_iter) == 0
    assert next(lazy_iter) == 1
    assert next(lazy_iter) == 0
    assert next(lazy_iter) == 1


def test_filter(f_iter):
    lazy_iter = f_iter.filter(lambda x: x % 2)
    assert next(lazy_iter) == 1
    assert next(lazy_iter) == 3
    assert next(lazy_iter) == 5


def test_enumerate(f_iter):
    lazy_iter = f_iter.enumerate()
    assert next(lazy_iter) == (0, 0)
    assert next(lazy_iter) == (1, 1)


def test_zip(f_iter):
    lazy_iter = f_iter.zip("abc")
    assert next(lazy_iter) == (0, "a")
    assert next(lazy_iter) == (1, "b")
    assert next(lazy_iter) == (2, "c")


def test_basic(f_iter):
    lazy_iter = f_iter.skip(2).take(5).skip(3)
    assert list(lazy_iter) == [5, 6]


def test_complex(f_iter):
    lazy_iter = (
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

    assert list(lazy_iter) == [(2, 12), (3, 13)]


def test_raise1(f_iter):
    with pytest.raises(IteratorExhaustedError):
        f_iter.take(5).skip(10)


def test_raise2(f_iter):
    with pytest.raises(IteratorExhaustedError):
        f_iter.skip(5).take(10).skip(15)
