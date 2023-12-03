import re
from operator import mul
from typing import Sequence, Iterable
from itertools import chain, product
import sys


def parse_symbols(input_: Sequence[str], pattern: str) -> Iterable[Sequence[int]]:
    return ([m.start(0) for m in re.finditer(pattern, row.strip())] for row_num, row in enumerate(input_))


def part1(input_: Sequence[str]) -> int:
    symbols_by_row = ([], *parse_symbols(input_, r'([^.\d])'), [])
    adjacencies = (
        {*r, *symbols_by_row[n - 1], *symbols_by_row[n + 1]} for n, r in enumerate(symbols_by_row[1:-1], 1)
    )
    return sum(
        int(match.group(0)) for row, symbols in zip(input_, adjacencies) for match in re.finditer(r'(\d+)', row)
        if any(match.start(0) - 1 <= symbol <= match.end(0) for symbol in symbols)
    )


def part2(input_: Sequence[str]) -> int:
    padded_input = ('.' * len(input_[0]), *input_, '.' * len(input_[-1]))

    def get_gear_ratio(row, col) -> int:
        try:
            return mul(*chain.from_iterable(
                get_horizontally_adjacent(col, padded_input[adj_row]) for adj_row in range(row, row + 3)
            ))
        except TypeError:
            return 0

    def get_horizontally_adjacent(col, string: str) -> Iterable[int]:
        left = re.findall(r'(\d+)$', string[:col])
        right = re.findall(r'^(\d+)', string[col+1:])
        if string[col].isdigit():
            yield int(''.join((*left, string[col], *right)))
        else:
            yield from (int(value) for value in chain(left, right))

    return sum(
        get_gear_ratio(*gear) for gear in chain.from_iterable(
            (product((row,), cols) for row, cols in enumerate(parse_symbols(input_, r'(\*)')))
        )
    )


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
