import sys
from itertools import accumulate, combinations
from typing import Tuple, Iterable


def parse_input(input_: Tuple[str, ...]) -> Tuple[Tuple[Tuple[int, int]], Tuple[int, ...], Tuple[int, ...]]:
    galaxies = ((col, row) for row, cols in enumerate(input_) for col, value in enumerate(cols) if value == '#')
    empty_rows = accumulate((all(char == '.' for char in row.strip()) for row in input_), initial=0)
    empty_cols = accumulate((all(cols[col] == '.' for cols in input_) for col in range(len(input_[0]))), initial=0)
    return tuple(galaxies), tuple(empty_rows), tuple(empty_cols)


def dist(g1: Tuple[int, int], g2: Tuple[int, int], empty_rows: Tuple[int, ...], empty_cols: Tuple[int, ...], stretch: int = 2) -> int:
    return sum(abs(x - y) for x, y in zip(g1, g2)) \
        + (stretch - 1) * (empty_cols[max(g1[0], g2[0]) + 1] - empty_cols[min(g1[0], g2[0])]) \
        + (stretch - 1) * (empty_rows[max(g1[1], g2[1]) + 1] - empty_rows[min(g1[1], g2[1])])


def part1(input_: Iterable[str]) -> int:
    galaxies, empty_rows, empty_cols = parse_input(tuple(input_))
    return sum(dist(g1, g2, empty_rows, empty_cols) for g1, g2 in combinations(galaxies, 2))


def part2(input_: Iterable[str]) -> int:
    galaxies, empty_rows, empty_cols = parse_input(tuple(input_))
    return sum(dist(g1, g2, empty_rows, empty_cols, 1_000_000) for g1, g2 in combinations(galaxies, 2))


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
