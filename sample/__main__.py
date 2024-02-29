# from argparse import ArgumentParser
from types import NoneType

from .sample import TRY, propagate


@propagate
def example_function(a, b):
    return TRY(a) + TRY(b)


if __name__ == "__main__":
    # parser = ArgumentParser()
    # parser.add_argument("--square", type=int, default=2)
    # args = parser.parse_args()
    print(example_function(5, 3))
    print(example_function(None, 3))
    print(example_function(5, None))
