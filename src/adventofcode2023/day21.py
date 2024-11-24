import sys
from functools import lru_cache
from typing import Tuple, Iterable, Sequence, Mapping, Dict, Collection
import heapq


def part1(input_: Iterable[str], target_steps: int = 64) -> int:
    map_ = tuple(row.strip() for row in input_)
    start = next((row, col) for row, line in enumerate(map_) for col, char in enumerate(line) if char == 'S')
    visited = reachable(map_, start)
    return sum((steps % 2) == (target_steps % 2) for steps in visited.values() if steps <= target_steps)



def reachable(
        map_: Sequence[Sequence[str]],
        start: Tuple[int, int]
) -> Mapping[Tuple[int, int], int]:
    visited = {start: 0}
    heapq.heapify(queue := [(dist, start) for start, dist in visited.items()])
    height, width = len(map_), len(map_[0])
    while queue:
        steps, cell = heapq.heappop(queue)
        for next_cell in (
                next_cell for next_cell in adjacent(*cell)
                if 0 <= next_cell[0] < width and 0 <= next_cell[1] < height
                and map_[next_cell[0] % height][next_cell[1] % width] != '#'
                and next_cell not in visited
        ):
            visited[next_cell] = steps + 1
            heapq.heappush(queue, (steps + 1, next_cell))
    return visited


def adjacent(row: int, col: int) -> Iterable[Tuple[int, int]]:
    return (
        (next_row, next_col) for next_row, next_col in ((row + 1, col), (row - 1, col), (row, col - 1), (row, col + 1))
    )


if __name__ == '__main__':
    #input_ = tuple(line.strip() for line in sys.stdin.readlines())
    with open('../../inputs/day21.txt', 'r') as fi:
        input_ = tuple(line.strip() for line in fi)
    print(part1(input_))
    print(part2(input_))