import sys
from itertools import accumulate, takewhile, islice, cycle
from math import lcm
from typing import Iterable, Tuple, Iterator, Mapping
import re

DIR_INDEX = {'L': 0, 'R': 1}


def parse_input(input_: Iterator[str]) -> Tuple[str, Mapping[str, Tuple[str, str]]]:
    return next(input_).strip(), {source: (left, right) for source, left, right in (
        re.findall(r'(\w+)', row) for row in islice(input_, 1, None)
    )}


def part1(input_: Iterable[str]) -> int:
    moves, adjs = parse_input(iter(input_))
    return sum(1 for _ in takewhile('ZZZ'.__ne__,
        accumulate(cycle(DIR_INDEX[dir_] for dir_ in moves), lambda pos, dir_: adjs[pos][dir_], initial='AAA')
    ))


def part2(input_: Iterable[str]) -> int:
    moves, adjs = parse_input(iter(input_))
    return lcm(*(
        sum(1 for _ in takewhile(lambda position: not position.endswith('Z'),
            accumulate(cycle(DIR_INDEX[dir_] for dir_ in moves), lambda pos, dir_: adjs[pos][dir_], initial=initial)
        )) for initial in adjs if initial.endswith('A')
    ))


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
