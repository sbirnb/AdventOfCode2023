import sys
from functools import reduce
from itertools import groupby, islice, batched, chain
from typing import Iterable, Tuple, Sequence, Iterator
import re


def parse_input(input_: Iterator[str]) -> Tuple[Iterable[Tuple[Tuple[int, int, int]]], Iterable[int]]:
    seeds = (int(seed) for seed in re.findall(r'(\d+)', next(input_)))
    mappings = (
        tuple(
            tuple(int(term) for term in re.findall(r'(\d+)', row))[:3]
            for row in islice(map_group[1], 1, None)
        )
        for map_group in groupby((row.strip() for row in input_), lambda x: bool(x)) if map_group[0]
    )
    return mappings, seeds


def part1(input_: Iterable[str]) -> int:
    return min(reduce(
        lambda values, mappings: tuple(next((
            dest + delta for dest, source, len_ in mappings if 0 <= (delta := value - source) < len_
        ), value) for value in values),
        *parse_input(iter(input_))
    ))


def part2(input_: Iterable[str]) -> int:

    def intersect(interval1, interval2):
        if interval1[1] <= interval2[0] or interval2[1] <= interval1[0]:
            return 0, 0
        return max(interval1[0], interval2[0]), min(interval1[1], interval2[1])

    def subtract_subinterval(interval, subinterval):
        if subinterval[0] == subinterval[1]:
            yield interval
            return
        if interval[0] < subinterval[0]:
            yield interval[0], subinterval[0]
        if subinterval[1] < interval[1]:
            yield subinterval[1], interval[1]

    def apply_mapping(intervals, mapping):
        new_unmapped, new_mapped = zip(*((
            subtract_subinterval(interval, (intersection := intersect(interval, mapping[0]))),
            tuple(end + mapping[1] for end in intersection)
        ) for interval in intervals[0]))
        return chain.from_iterable(new_unmapped),\
            chain(intervals[1], filter(lambda interval: interval[0] != interval[1], new_mapped))

    mappings, seeds = parse_input(iter(input_))

    return min(reduce(
        lambda intervals, mappings: chain.from_iterable(reduce(apply_mapping, mappings, (intervals, tuple()))), (
            (((source, source + len_), target - source) for target, source, len_ in mapping_group)
            for mapping_group in mappings
        ), ((start, start + len_) for start, len_ in batched(seeds, 2))
    ))[0]


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
