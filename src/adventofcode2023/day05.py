import sys
from functools import reduce
from itertools import groupby, islice, batched, permutations, chain
from typing import Iterable, Tuple, Sequence, Iterator, Optional
import re


def apply_mappings(values: Sequence[int], mappings: Sequence[Tuple[int, int]]) -> Sequence[int]:
    return tuple(next((
        dest + delta for dest, source, len_ in mappings if 0 <= (delta := value - source) < len_
    ), value) for value in values)


def parse_input(input_: Iterator[str]) -> Tuple[Iterable[Iterable[Tuple[int, int, int]]], Iterable[int]]:
    seeds = (int(seed) for seed in re.findall(r'(\d+)', next(input_)))
    mappings = (
        tuple(
            tuple(int(term) for term in re.findall(r'(\d+)', row))[:3]
            for row in islice(map_group[1], 1, None)
        )
        for map_group in groupby((row.strip() for row in input_), lambda x: bool(x)) if map_group[0]
    )
    return (mappings, seeds)


def part1(input_: Iterable[str]) -> int:
    return min(reduce(apply_mappings, *parse_input(iter(input_))))


def part2(input_: Iterable[str]) -> int:

    Interval = Tuple[int, int]

    def shift(interval: Optional[Interval], by: int) -> Optional[Interval]:
        if interval is None:
            return None
        return interval[0] + by, interval[1] + by

    def intersect(interval1: Interval, interval2: Interval) -> Optional[Interval]:
        if interval1[1] <= interval2[0] or interval2[1] <= interval1[0]:
            return None
        else:
            return max(interval1[0], interval2[0]), min(interval1[1], interval2[1])

    def subtract_subinterval(interval: Interval, subinterval: Interval) -> Iterator[Interval]:
        if subinterval is None:
            yield interval
            return
        if interval[0] < subinterval[0]:
            yield interval[0], subinterval[0]
        if subinterval[1] < interval[1]:
            yield subinterval[1], interval[1]

    mappings, seeds = parse_input(iter(input_))
    seed_intervals = ((start, start + len_) for start, len_ in batched(seeds, 2))
    mapping_intervals = (
        (((source, source + len_), target - source) for target, source, len_ in mapping_group)
        for mapping_group in mappings
    )

    intervals = seed_intervals
    for mapping_block in mapping_intervals:
        unmapped, mapped = intervals, tuple()
        for map_source, offset in mapping_block:
            for interval in unmapped:
                intersection = intersect(interval, map_source)
                unmapped = (*islice(unmapped, 1, None), *subtract_subinterval(interval, intersection))
                if intersection:
                    mapped = (*mapped, shift(intersection, offset))
        intervals = chain(unmapped, mapped)

    return min(intervals)[0]


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
