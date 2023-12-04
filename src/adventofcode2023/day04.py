import sys
from functools import reduce
from typing import Iterable
import re
from itertools import repeat, zip_longest


def parse_scores(input_: Iterable[str]) -> Iterable[int]:
    return (len(reduce(
        set.intersection, (
            set(re.findall(r'(\d+)', group))
            for group in re.match(r'Card +\d+:([\d ]+)\|([\d ]+)', row).groups()
        )
    )) for row in input_)


def part1(input_: Iterable[str]) -> int:
    return sum(2 ** (hits - 1) for hits in parse_scores(input_) if hits)


def part2(input_: Iterable[str]) -> int:

    def count_tickets():
        copies = iter([])
        for score in parse_scores(input_):
            n_tickets = next(copies, 0) + 1
            yield n_tickets
            copies = ((new or 0) + (old or 0) for new, old in zip_longest(repeat(n_tickets, score), copies))

    return sum(count_tickets())


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
