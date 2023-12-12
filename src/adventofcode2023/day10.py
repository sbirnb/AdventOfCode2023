import sys
from itertools import batched, pairwise, chain
from typing import Iterable, Mapping, Tuple

NORTH, SOUTH, EAST, WEST = -1j, 1j, 1, -1

IN_DIRS = {
    '|': {NORTH, SOUTH},
    '-': {EAST, WEST},
    'L': {SOUTH, WEST},
    'J': {SOUTH, EAST},
    '7': {NORTH, EAST},
    'F': {NORTH, WEST},
    '.': set(),
    'S': {NORTH, SOUTH, EAST, WEST}
}


def parse_input(input_: Iterable[str]) -> Mapping[complex, str]:
    return {
        complex(col, row): value for row, cols in enumerate(input_) for col, value in enumerate(cols)
    }


def path(map_: Mapping[complex, str], pos_: complex, dir_: complex) -> Iterable[Tuple[complex, complex]]:
    while (pipe := map_[pos_ := pos_ + dir_]) != 'S':
        yield pos_, (dir_ := -next(iter(IN_DIRS[pipe] - {dir_})))


def find_start(map_: Mapping[complex, str]) -> Tuple[complex, complex]:
    pos = next(pos for pos, pipe in map_.items() if pipe == 'S')
    return pos, next(dir_ for dir_ in (NORTH, SOUTH, EAST, WEST) if dir_ in IN_DIRS[map_.get(pos + dir_, '.')])


def part1(input_: Iterable[str]) -> int:
    map_ = parse_input(input_)
    pos, dir_ = find_start(map_)
    return sum(1 for _ in zip(path(map_, pos, dir_), batched(path(map_, pos, dir_), 2)))


def part2(input_: Iterable[str]) -> int:
    map_ = parse_input(input_)
    start = find_start(map_)
    return 1 + abs(sum(
        (end.imag - start.imag) * start.real for start, end in
        pairwise(pos for pos, _ in chain((start,), path(map_, *start), (start,)))
    )) - (sum(1 for _ in path(map_, *start)) + 1) / 2


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
