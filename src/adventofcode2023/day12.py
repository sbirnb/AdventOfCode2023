import sys
from functools import lru_cache
from itertools import groupby, chain, takewhile
from typing import Iterable, Tuple, Sequence, Optional


def parse_input(input_: Iterable[str]) -> Iterable[Tuple[Sequence[Tuple[str, int]], Sequence[int]]]:
    return (
        (
            tuple((tub_type, sum(1 for _ in tubs)) for tub_type, tubs in groupby(tub_str)),
            tuple(int(broken) for broken in broken_str.split(','))
        )
        for tub_str, broken_str in (row.strip().split(' ') for row in input_)
    )


def count_ways(all_tubs: Sequence[Tuple[str, int]], all_broken: Sequence[int]) -> int:

    def check(
            tubs: Sequence[Tuple[str, int]], broken: Sequence[int], tubs_min: int, tubs_max: int, broken_total: int
    ) -> Optional[int]:
        if broken_total > tubs_max or broken_total < tubs_min:
            return 0
        if not tubs:
            return all(n_broken == 0 for n_broken in broken)
        if not broken:
            return all(tub_type in '.?' for tub_type, _ in tubs)
        return None

    @lru_cache(maxsize=None)
    def count_open(
            tubs: Sequence[Tuple[str, int]], broken: Sequence[int], tubs_min: int, tubs_max: int, broken_total: int
    ) -> int:
        if (ways := check(tubs, broken, tubs_min, tubs_max, broken_total)) is not None:
            return ways
        tub_type, n_tubs = tubs[0]
        n_broken = broken[0]
        if n_tubs == 0:
            return count_open(tubs[1:], broken, tubs_min, tubs_max, broken_total)
        if tub_type == '.':
            if n_broken == 0:
                return count_closed(tubs[1:], broken[1:], tubs_min, tubs_max, broken_total)
            return 0
        if tub_type == '#':
            if n_tubs > n_broken:
                return 0
            return count_open(
                tubs[1:], (n_broken - n_tubs, *broken[1:]),
                tubs_min - n_tubs, tubs_max - n_tubs, broken_total - n_tubs
            )
        if tub_type == '?':
            if n_broken == 0:
                return count_closed(
                    ((tub_type, n_tubs - 1), *tubs[1:]), broken[1:],
                    tubs_min, tubs_max - 1, broken_total
                )
            return count_open(
                ((tub_type, n_tubs - (used := min(n_tubs, n_broken))), *tubs[1:]), (n_broken - used, *broken[1:]),
                tubs_min, tubs_max - used, broken_total - used
            )

    @lru_cache(maxsize=None)
    def count_closed(
            tubs: Sequence[Tuple[str, int]],
            broken: Sequence[int],
            tubs_min: int,
            tubs_max: int,
            broken_total: int
    ) -> int:
        if (ways := check(tubs, broken, tubs_min, tubs_max, broken_total)) is not None:
            return ways
        tub_type, n_tubs = tubs[0]
        if tub_type == '.':
            return count_closed(tubs[1:], broken, tubs_min, tubs_max, broken_total)
        if tub_type == '#':
            return count_open(tubs, broken, tubs_min, tubs_max, broken_total)
        if tub_type == '?':
            return sum(takewhile(
                lambda new_ways: len(tubs) <= 1 or tubs[1][0] != '.' or new_ways > 0,
                (count_open(
                    ((tub_type, n_tubs - skip), *tubs[1:]), broken,
                    tubs_min, tubs_max - skip, broken_total
                ) for skip in range(n_tubs))
            )) + count_closed(tubs[1:], broken, tubs_min, tubs_max - n_tubs, broken_total)

    @lru_cache(maxsize=None)
    def get_tubs_min(tubs: Sequence[Tuple[str, int]]) -> int:
        return sum(n_tubs for tub_type, n_tubs in tubs if tub_type == '#')

    @lru_cache(maxsize=None)
    def get_tubs_max(tubs: Sequence[Tuple[str, int]]) -> int:
        return sum(n_tubs for tub_type, n_tubs in tubs if tub_type in '#?')

    @lru_cache(maxsize=None)
    def get_total_broken(broken: Sequence[int]) -> int:
        return sum(broken)

    def solve(tubs: Sequence[Tuple[str, int]], broken: Sequence[int]) -> int:
        return count_closed(
            tubs,
            broken,
            get_tubs_min(tubs),
            get_tubs_max(tubs),
            get_total_broken(broken)
        )

    broken_tub_groups = tuple(
        tuple(grouping) for is_broken, grouping in groupby(all_tubs, lambda tubs: tubs[0] != '.') if is_broken
    )

    @lru_cache(maxsize=None)
    def solve_by_group(tub_group_index: int, broken_index: int) -> int:
        if tub_group_index == len(broken_tub_groups) - 1:
            return solve(broken_tub_groups[tub_group_index], all_broken[broken_index:])
        max_tubs_remaining = sum(get_tubs_max(tub_group) for tub_group in broken_tub_groups[tub_group_index:])

        ways = 0
        for end_broken_index in range(broken_index, len(all_broken) + 1):
            broken_remaining = get_total_broken(all_broken[end_broken_index:])
            if broken_remaining > max_tubs_remaining:
                continue
            group_ways = solve(broken_tub_groups[tub_group_index], all_broken[broken_index:end_broken_index])
            if group_ways:
                ways += group_ways * solve_by_group(tub_group_index + 1, end_broken_index)

        return ways

    return solve_by_group(0, 0)


def part1(input_: Iterable[str]) -> int:
    return sum(count_ways(*row) for row in parse_input(input_))


def part2(input_: Iterable[str]) -> int:
    return sum(count_ways(
        tuple(chain(tubs, (('?', 1),), tubs, (('?', 1),), tubs, (('?', 1),), tubs, (('?', 1),), tubs))
        , broken * 5
    ) for tubs, broken in parse_input(input_))


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
