from dataclasses import dataclass
from types import NoneType

from sample.sample import TRY, propagate


@propagate(NoneType)
def try_add(a, b):
    return TRY(a) + TRY(b)


@propagate(NoneType)
def try_sub(a, b):
    return TRY(a) - TRY(b)


def test_propagate():
    assert try_add(5, 3) == 8
    assert try_add(None, 3) is None
    assert try_add(5, None) is None

    a = 1
    assert try_add(a := a + 1, a := a + 1) == 5
    assert try_sub(a := a + 1, a := a + 1) == -1


@dataclass
class Error:
    msg: str


@propagate(Error)
def try_add1(arg0, arg1):
    arg0 = Error("arg0 equals 2") if arg0 == 2 else arg0
    arg1 = Error("arg1 equals 3") if arg1 == 3 else arg1
    return TRY(arg0) + TRY(arg1)


def test_custom_error():
    assert try_add1(1, 4) == 5
    assert try_add1(2, 4) == Error("arg0 equals 2")
    assert try_add1(1, 3) == Error("arg1 equals 3")
