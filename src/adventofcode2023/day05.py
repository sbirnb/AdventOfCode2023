from itertools import groupby, islice
from typing import Iterable, Tuple, Sequence
import re


def apply_mappings(mappings: Iterable[Tuple[int, int, int]], input_: int) -> int:
    return next((
        dest + delta for dest, source, len_ in mappings if 0 <= (delta := input_ - source) < len_
    ), input_)


def parse_input(input_: Iterable[str]) -> Tuple[Iterable[int], Iterable[Iterable[Tuple[int, int, int]]]]:
    iter_input = iter(input_)
    seeds = (int(seed) for seed in re.findall(r'(\d+)', next(iter_input)))
    mappings = (
        tuple(
            tuple(int(term) for term in re.findall(r'(\d+)', row))
            for row in islice(map_group[1], 1, None)
        )
        for map_group in groupby((row.strip() for row in iter_input), lambda x: bool(x)) if map_group[0]
    )
    return seeds, mappings

def part1(input_: Iterable[str]) -> int:
    items, mappings = parse_input(input_)

    for mapping_group in mappings:
        items = (apply_mappings(mapping_group, item) for item in items)
    return min(items)

if __name__ == '__main__':
    input_ = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''.split('\n')
    print(parse_input(input_))


