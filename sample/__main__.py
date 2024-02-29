# from argparse import ArgumentParser
from types import NoneType

from .sample import TRY, propagate


@propagate(NoneType)
def try_add(a, b):
    return TRY(a) + TRY(b)


if __name__ == "__main__":
    # parser = ArgumentParser()
    # parser.add_argument("--square", type=int, default=2)
    # args = parser.parse_args()
    print(try_add(5, 3))
    print(try_add(None, 3))
    print(try_add(5, None))
