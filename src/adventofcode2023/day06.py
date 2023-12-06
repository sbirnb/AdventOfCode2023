import re
import sys
from math import sqrt, ceil, floor, prod
from typing import Tuple, Iterable
from operator import sub


def bounds(time: int, distance: int) -> Tuple[int, int]:
    sqrt_desc = sqrt(time * time - 4 * distance)
    return ceil((time - sqrt_desc) / 2 + 1e-10), floor((time + sqrt_desc) / 2 - 1e-10)


def part1(input_: Iterable[str]) -> int:
    return prod(
        (b := bounds(*race))[1] - b[0] + 1 for race in
        zip(*((int(n) for n in re.findall(r'(\d+)', row)) for row in input_))
    )


def part2(input_: Iterable[str]) -> int:
    return 1 - sub(*bounds(*(int(re.sub(r'[^\d]', '', row)) for row in input_)))


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
