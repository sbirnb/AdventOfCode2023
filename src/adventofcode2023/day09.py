import re
import sys
from itertools import pairwise, accumulate, count, takewhile, chain, cycle
from typing import Iterable


def parse_input(input_: Iterable[str]) -> Iterable[Iterable[int]]:
    return ((int(value) for value in re.findall(r'(-?\d+)', row)) for row in input_)


def part1(input_: Iterable[str]) -> int:
    return sum(deltas[-1] for deltas in chain.from_iterable(takewhile(
        bool, accumulate(count(), lambda seqs, _: tuple(x2 - x1 for x1, x2 in pairwise(seqs)), initial=tuple(sequence))
    ) for sequence in parse_input(input_)))


def part2(input_: Iterable[str]) -> int:
    return sum(chain.from_iterable((sign * deltas[0] for sign, deltas in zip(cycle((1, -1)), takewhile(
        bool,
        accumulate(count(), lambda seqs, _: tuple(x2 - x1 for x1, x2 in pairwise(seqs)), initial=tuple(sequence))
    ))) for sequence in (tuple(sequence) for sequence in parse_input(input_))))


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
