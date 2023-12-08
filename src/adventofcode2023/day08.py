import sys
from itertools import accumulate, takewhile, islice, cycle
from typing import Iterable, Tuple, Iterator
import re

DIR_INDEX = {'L': 0, 'R': 1}

def parse_input(input_: Iterator[str]) -> Tuple[str, Iterable[Tuple[str, Tuple[str, str]]]]:
    return next(input_).strip(), dict(
        (source, (left, right)) for source, left, right in
        (re.findall(r'([A-Z]+)', row) for row in islice(input_, 1, None))
    )


def part1(input_: Iterable[str]) -> int:
    moves, adjs = parse_input(iter(input_))
    return sum(1 for _ in takewhile(
        'ZZZ'.__ne__,
        accumulate(cycle(DIR_INDEX[dir_] for dir_ in moves), lambda pos, dir_: adjs[pos][dir_], initial='AAA')
    ))

def part2(input_: Iterable[str]) -> int:
    moves, adjs = parse_input(iter(input_))
    return sum(

    )


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))