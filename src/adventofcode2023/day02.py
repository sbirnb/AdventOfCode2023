import re
from functools import reduce
from typing import Tuple, Iterable, Mapping
from itertools import chain
import sys
from operator import mul


def parse_game(game: str) -> Tuple[int, Iterable[Iterable[Tuple[str, int]]]]:
    game_id, rounds = re.match(r'Game (\d+): (.*)$', game).groups()
    return int(game_id), (
        (
            (color, int(qty)) for qty, color in
            (cube.strip().split(' ') for cube in round_.strip().split(', '))
        )
        for round_ in rounds.split('; ')
    )


def part1(input_: Iterable[str], constraints: Mapping[str, int]) -> int:
    return sum(
        id_ for id_, rounds in (parse_game(row) for row in input_)
        if all(qty <= constraints.get(color, 0) for color, qty in chain.from_iterable(rounds))
    )


def part2(input_: Iterable[str]) -> int:
    def get_power(game: str) -> int:
        n_cubes = {}
        for qty, color in re.findall(r'(\d+) (\w+)', game):
            n_cubes[color] = max(int(qty), n_cubes.get(color, 0))
        return reduce(mul, n_cubes.values())
    return sum(get_power(game) for game in input_)


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_, {'red': 12, 'green': 13, 'blue': 14}))
    print(part2(input_))
