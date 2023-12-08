import sys
from collections import Counter
from itertools import count
from typing import Iterable, Tuple, Mapping


def parse_input(input_: Iterable[str], values: Mapping[str, int]) -> Iterable[Tuple[Tuple[int, ...], int]]:
    return ((tuple(values[card] for card in hand), int(bid)) for hand, bid in (row.strip().split() for row in input_))


def part1(input_: Iterable[str]) -> int:

    def score(hand: Tuple[int, ...]) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
        n_kinds = Counter(Counter(hand).values())
        return tuple(n_kinds[n] for n in range(5, 0, -1)), hand

    values = dict(zip('23456789TJQKA', count()))
    return sum(rank * hand[1] for rank, hand in enumerate(sorted(parse_input(input_, values), key=lambda hand: score(hand[0])), 1))


def part2(input_: Iterable[str]) -> int:

    def score(hand: Tuple[int, ...]) -> Tuple[int, Tuple[int, ...]]:
        counts = Counter(hand)
        j_count = counts[0]
        n_kinds = Counter(value for card, value in counts.items() if card != 0)
        if j_count == 5 or any(n + j_count >= 5 for n in range(6) if n_kinds[n] > 0):
            return 6, hand
        if any(n + j_count >= 4 for n in range(6) if n_kinds[n] > 0):
            return 5, hand
        if (j_count == 1 and n_kinds[2] > 1) or (n_kinds[3] > 0 and n_kinds[2] > 0):
            return 4, hand
        if any(n + j_count >= 3 for n in range(6) if n_kinds[n] > 0):
            return 3, hand
        if n_kinds[2] + (j_count > 0) >= 2:
            return 2, hand
        if n_kinds[2] > 0 or j_count > 0:
            return 1, hand
        return 0, hand

    values = dict(zip('J23456789TQKA', count()))
    return sum(rank * hand[1] for rank, hand in enumerate(sorted(parse_input(input_, values), key=lambda hand: score(hand[0])), 1))


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
