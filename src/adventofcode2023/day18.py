import sys
from itertools import accumulate, pairwise
from typing import Iterable, Tuple, Sequence
import re


def get_volume(moves: Sequence[Tuple[str, int]]) -> int:
    segments = tuple(pairwise(accumulate(moves, lambda pos, move: pos + move[0] * move[1], initial=0)))
    return int(
        abs(sum((p1.real - p2.real) * p1.imag for p1, p2 in segments if p1.imag == p2.imag))
        + sum(abs(p1.real - p2.real + p1.imag - p2.imag) for p1, p2 in segments) // 2 + 1
    )


def part1(input_: Iterable[str]) -> int:
    dirs = dict(zip('UDLR', (-1j, 1j, -1, 1)))
    return get_volume(tuple(
        (dirs[dir_], int(dist)) for dir_, dist in (re.match(r'(\w) (\d+)', row).groups() for row in input_)
    ))


def part2(input_: Iterable[str]) -> int:
    return get_volume(tuple(
        ((1, 1j, -1, -1j)[int(dir_)], int(dist, 16))
        for dist, dir_ in (re.search(r'\(#(\w{5})(\w)\)', row).groups() for row in input_))
    )


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
