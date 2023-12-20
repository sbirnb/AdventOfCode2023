import math
import sys
from collections import defaultdict
from heapq import heappop, heappush
from random import random
from typing import Iterable, Mapping


def parse_input(input_: Iterable[str]) -> Mapping[complex, int]:
    return {complex(col, row): int(value) for row, values in enumerate(input_) for col, value in enumerate(values.strip())}


def get_best_path(map_: Mapping[complex, int], min_run: int, max_run: int) -> int:
    queue = [(0, random(), 0, 1, 0, (0,)), (0, random(), 0, 1j, 0, (0,))]

    target = complex(max(pos.real for pos in map_), max(pos.imag for pos in map_))
    best = defaultdict(lambda: math.inf)
    visited = set()
    while queue:
        cost, _, pos, dir_, heat, chain = heappop(queue)
        if pos == target:
            return heat
        if (pos, dir_) not in visited:
            visited.add((pos, dir_))
            new_heat = heat
            for dist in range(1, max_run + 1):
                new_pos = pos + dist * dir_
                if new_pos not in map_:
                    break
                new_heat += map_[new_pos]
                if dist < min_run:
                    continue
                for new_dir in (dir_ * 1j, dir_ * -1j):
                    if new_heat < best[new_pos, new_dir]:
                        heappush(queue, (
                            new_heat + abs(new_pos.real - target.real) + abs(new_pos.imag - target.imag), random(),
                            new_pos, new_dir, new_heat, chain + (new_pos,)
                        ))
                        best[new_pos, new_dir] = new_heat


def part1(input_: Iterable[str]) -> int:
    map_ = parse_input(input_)
    return get_best_path(map_, 1, 3)


def part2(input_: Iterable[str]) -> int:
    map_ = parse_input(input_)
    return get_best_path(map_, 4, 10)


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
