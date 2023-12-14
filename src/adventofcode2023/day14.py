import sys
from functools import reduce
from itertools import islice
from typing import Tuple, Iterable, Sequence
from collections import Counter


def part1(input_: Iterable[str]) -> int:
    def update_state(state: Tuple[int, int], row: int, stone: str) -> Tuple[int, int]:
        weight, n_stones = state
        if stone == '.':
            return weight + n_stones, n_stones
        if stone == 'O':
            return weight + row, n_stones + 1
        if stone == '#':
            return weight, 0
    state = tuple(row.strip() for row in input_)
    return sum(weight for weight, _ in reduce(
        lambda states, updates: tuple(
            update_state(state, updates[0], stone) for state, stone in zip(states, updates[1]))
        , enumerate(reversed(state), 1),
        ((0, 0),) * len(state[-1])
    ))


def part2(input_: Iterable[str]) -> int:

    def states(initial_state: Sequence[str]) -> Iterable[Sequence[str]]:
        state = initial_state
        while True:
            yield state
            for _ in range(4):
                state = tuple(
                    '#'.join('.' * count['.'] + 'O' * count['O'] for count in (Counter(segment) for segment in row.split('#')))
                    for row in (''.join(reversed(row)) for row in zip(*state))
                )

    def get_cycle_start(initial_state: Sequence[str]) -> Tuple[int, Sequence[str]]:
        visited = dict()
        for iteration, state in enumerate(states(initial_state)):
            if state in visited:
                return visited[state], state
            visited[state] = iteration

    pre_cycle_iterations, cycle_start_state = get_cycle_start(tuple(row.strip() for row in input_))
    period_length = next(
            iteration for iteration, state in enumerate(islice(states(cycle_start_state), 1, None), 1)
            if state == cycle_start_state
    )
    for _, final_state in zip(range((1000000000 - pre_cycle_iterations) % period_length + 1), states(cycle_start_state)):
        pass
    return sum(row.count('O') * n for n, row in enumerate(reversed(final_state), 1))


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))