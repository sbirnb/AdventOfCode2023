import math
import sys
from functools import lru_cache
from itertools import takewhile
from typing import Iterable, Tuple, Sequence
import re
import bisect


def parse_input(input_: Iterable[str]) -> Iterable[Tuple[str, Sequence[int]]]:
    return (
        (tubs, tuple(int(broken) for broken in broken_str.split(',')))
        for tubs, broken_str in (row.strip().split(' ') for row in input_)
    )


def count_ways(tubs: str, broken: Sequence[int]) -> int:
    tubs = tubs + '.'

    positions = {
        length: tuple(
            start for start in range(len(tubs) - length + 1)
            if all(tubs[i] in '?#' for i in range(start, start + length))
            and tubs[start - 1] != '#' and tubs[start + length] != '#'
        ) for length in set(broken)
    }
    hashes = tuple(match.start(0) for match in re.finditer(r'(^#|(?<!#)#)', tubs))

    @lru_cache(maxsize=None)
    def solve(tubs_index: int, broken_index: int) -> int:
        if (not hashes or tubs_index > hashes[-1]) and broken_index == len(broken):
            return 1
        if broken_index == len(broken):
            return 0
        length = broken[broken_index]
        start_positions = positions[length]
        next_hash = (hashes + (math.inf,))[bisect.bisect_left(hashes, tubs_index)]
        return sum(solve(start + length + 1, broken_index + 1) for start in takewhile(
            lambda start: start <= next_hash,
            start_positions[bisect.bisect_left(start_positions, tubs_index):]
        ))
    return solve(0, 0)


def part1(input_: Iterable[str]) -> int:
    return sum(count_ways(*row) for row in parse_input(input_))


def part2(input_: Iterable[str]) -> int:
    return sum(count_ways('?'.join((tubs,) * 5), broken * 5) for tubs, broken in parse_input(input_))


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
