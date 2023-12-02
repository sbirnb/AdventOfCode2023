import re
from functools import reduce
from typing import Iterable, Mapping
import sys
from operator import mul


def part1(input_: Iterable[str], constraints: Mapping[str, int]) -> int:
    return sum(
        int(game.split(' ')[1]) for game, rounds in (row.split(': ') for row in input_)
        if all(int(qty) <= constraints.get(color, 0) for qty, color in re.findall(r'(\d+) (\w+)', rounds))
    )


def part2(input_: Iterable[str]) -> int:
    return sum(reduce(mul, (reduce(
        (lambda acc_max, val_color: {**acc_max, val_color[1]: max(int(val_color[0]), acc_max.get(val_color[1], 0))}),
        re.findall(r'(\d+) (\w+)', game),
        dict()
    ).values())) for game in input_)


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_, {'red': 12, 'green': 13, 'blue': 14}))
    print(part2(input_))
