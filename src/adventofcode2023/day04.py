import sys
from typing import Iterable
import re


def part1(input_: Iterable[str]) -> int:
    return sum(
        2 ** (hits - 1)
        for row in input_
        if (hits := (lambda winners, have: sum(n in set(winners) for n in have))(
            *(re.findall(r'(\d+)', group) for group in re.match(r'Card +\d+:([\d ]+)\|([\d ]+)', row).groups())
        ))
    )


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
