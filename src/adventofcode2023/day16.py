import sys
from collections import defaultdict
from functools import reduce
from itertools import chain
from typing import Iterable, Mapping, Set, Tuple

MIRRORS = {
    '/': lambda dir_: {{1: -1j, -1j: 1, -1: 1j, 1j: -1}[dir_]},
    '\\': lambda dir_: {{1: 1j, 1j: 1, -1: -1j, -1j: -1}[dir_]},
    '-': lambda dir_: {dir_} if dir_.imag == 0 else {-1, 1},
    '|': lambda dir_: {dir_} if dir_.real == 0 else {-1j, 1j},
    '.': lambda dir_: {dir_}
}


def parse_input(input_: Iterable[str]) -> Mapping[complex, str]:
    return {
        complex(col, row): value for row, values in enumerate(input_) for col, value in enumerate(values.strip())
    }


def part1(input_: Iterable[str]) -> int:
    parsed = parse_input(input_)
    visited = defaultdict(set)
    stack = [(-1, 1)]
    while stack:
        pos, dir_ = stack.pop()
        if (next_pos := pos + dir_) in parsed:
            visited[next_pos].update(next_dirs := MIRRORS[parsed[next_pos]](dir_) - visited[next_pos])
            stack.extend((next_pos, next_dir) for next_dir in next_dirs)
    return len(visited)


def part2(input_: Iterable[str]) -> int:
    parsed = parse_input(input_)
    downstream_states = dict()
    loops = set()

    def get_downstream(start_state: Tuple[complex, complex]) -> Set[complex]:
        in_stack = {start_state}
        stack = [start_state]
        while stack:
            pos, dir_ = state = stack[-1]
            if (next_pos := pos + dir_) not in parsed:
                in_stack.remove(state)
                downstream_states[stack.pop()] = frozenset({state})
                continue
            next_states = tuple((next_pos, next_dir) for next_dir in MIRRORS[parsed[next_pos]](dir_))
            for next_state in next_states:
                if next_state in in_stack:
                    loops.add(next_state)
                    downstream_states[next_state] = frozenset({next_state})
                elif next_state not in downstream_states:
                    in_stack.add(next_state)
                    stack.append(next_state)
            if stack[-1] != state:
                continue
            in_stack.remove(state)
            downstream_states[stack.pop()] = frozenset({state}) | reduce(frozenset.union, (downstream_states[next_state] for next_state in next_states))
        downstream = downstream_states[start_state]
        positions = {state[0] for state in chain(downstream, chain.from_iterable(downstream_states[loop_node] for loop_node in loops & downstream))}

        return positions

    height = int(max(pos.imag for pos in parsed) + 1)
    width = int(max(pos.real for pos in parsed) + 1)

    return max(len(get_downstream(state)) for state in chain(
        ((-1 + row * 1j, 1) for row in range(height)),
        ((width + row * 1j, -1) for row in range(height)),
        ((col - 1j , 1j) for col in range(width)),
        ((col + height * 1j, -1j) for col in range(width))
    )) - 1


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
