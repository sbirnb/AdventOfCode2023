import math
import sys
from itertools import groupby, count
from typing import Iterable, Tuple, Mapping, Sequence
import re
from operator import gt, lt

def parse_input(input_: Iterable[str]) -> Tuple[Sequence[Tuple[str, Tuple[str, str, int, str, str]]], Mapping[str, int]]:
    workflows, parts = (
        tuple(t) for t in (value for include, value in groupby((row.strip() for row in input_), key=bool) if include)
    )
    return tuple(
        (f'{name}.{i}', (
            attr, cmp, int(val or '0'),
            target if target in {'A', 'R'} else f'{target}.0',
            default if default in {'A', 'R'} else f'{default}.0' if default else f'{name}.{i + 1}'
        ))
        for name, rules in (re.match(r'(\w+)\{(.*)\}', row).groups() for row in workflows)
        for i, (attr, cmp, val, target, default) in enumerate(re.findall(r'([xmas])([<>])(\d+):(\w+),(?=(\w+)$)?', rules))
    ), tuple({key: int(value) for key, value in re.findall(r'(\w)=(\d+),?', part)} for part in parts)


def part1(input_: Iterable[str]) -> int:
    cmps = {'<': lt, '>': gt}
    transforms, parts = parse_input(input_)
    transform_map = dict(transforms)

    def resolve(part: Mapping[str, int]):
        next_rule = 'in.0'
        while next_rule not in 'AR':
            attr, cmp, val, next_, default = transform_map[next_rule]
            if cmps[cmp](part[attr], val):
                next_rule = next_
            else: next_rule = default
        return next_rule == 'A'
    return sum(sum(part.values()) for part in parts if resolve(part))


def part2(input_: Iterable[str]) -> int:
    transforms, _ = parse_input(input_)
    transform_map = dict(transforms)
    attr_indexes = dict(zip('xmas', count()))

    def get_bounds(rule: str, bounds: Sequence[Tuple[int, int]]):
        if rule == 'A':
            yield bounds
            return
        if rule == 'R':
            return
        attr, cmp, val, next_, default = transform_map[rule]
        attr_index = attr_indexes[attr]
        b_lower, b_upper = bounds[attr_index]
        if cmp == '<':
            yield from get_bounds(next_, (*bounds[:attr_index], (b_lower, val), *bounds[attr_index + 1:]))
            yield from get_bounds(default, (*bounds[:attr_index], (val, b_upper), *bounds[attr_index + 1:]))
        elif cmp == '>':
            yield from get_bounds(next_, (*bounds[:attr_index], (val + 1, b_upper), *bounds[attr_index + 1:]))
            yield from get_bounds(default, (*bounds[:attr_index], (b_lower, val + 1), *bounds[attr_index + 1:]))

    def intersect_ranges(range1: Tuple[int, int], range2: Tuple[int, int]) -> Tuple[int, int]:
        if range2 < range1:
            return intersect_ranges(range2, range1)
        return range2[0], max(range2[0], range1[1])

    return sum(
        (math.prod(max(0, upper - lower) for lower, upper in range))
        for range in get_bounds('in.0', tuple((1, 4001) for _ in 'xmas'))
    )


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
