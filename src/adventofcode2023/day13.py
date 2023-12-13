import sys
from itertools import groupby, chain
from typing import Iterable, Sequence


def parse_input(input_: Iterable[str]) -> Iterable[Sequence[str]]:
    return (tuple(row.strip() for row in group) for keep, group in groupby((row.strip() for row in input_), key=bool) if keep)


def get_reflection_size(rows: Sequence[str], smudges: int) -> int:
    return next(chain(
        (above for above in range(1, len(rows) // 2 + 1) if sum(first != last for first, last in zip(
            chain.from_iterable(rows[:above]), chain.from_iterable(rows[above * 2 - 1:above - 1:-1])
        )) == smudges),
        (len(rows) - below for below in range(1, len(rows) // 2 + 1) if sum(first != last for first, last in zip(
            chain.from_iterable(rows[-below:]), chain.from_iterable(rows[-below - 1:-2*below - 1:-1])
        )) == smudges)
    ), 0)


def part1(input_: Iterable[str]) -> int:
    originals, transposes = zip(*((rows, tuple(zip(*rows))) for rows in tuple(parse_input(input_))))
    return 100 * sum(get_reflection_size(rows, 0) for rows in originals) \
        + sum(get_reflection_size(rows, 0) for rows in transposes)


def part2(input_: Iterable[str]) -> int:
    originals, transposes = zip(*((rows, tuple(zip(*rows))) for rows in tuple(parse_input(input_))))
    return 100 * sum(get_reflection_size(rows, 1) for rows in originals) \
        + sum(get_reflection_size(rows, 1) for rows in transposes)


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
