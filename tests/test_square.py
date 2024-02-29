from types import NoneType

from sample.sample import TRY, propagate


@propagate
def try_add(a, b):
    return TRY(a) + TRY(b)


def test_propagate():
    assert try_add(5, 3) == 8
    assert try_add(None, 3) is None
    assert try_add(5, None) is None
