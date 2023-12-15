import sys
from dataclasses import dataclass, field
from functools import reduce
from itertools import chain
from typing import Iterable, Dict, Tuple
import re


def parse_intput(input_: Iterable[str]) -> Iterable[str]:
    return chain.from_iterable(row.strip().split(',') for row in input_)


def hash_(string: str) -> int:
    return reduce(lambda hash_, char: ((hash_ + ord(char)) * 17) % 256, string, 0)


def part1(input_: Iterable[str]) -> int:
    return sum(hash_(string) for string in parse_intput(input_))


@dataclass
class Box:
    size: int = 0
    lenses: Dict[str, Tuple[int, int]] = field(default_factory=dict)

    def add(self, label: str, focal: int):
        self.size += 1
        position = self.lenses.get(label, (0, self.size))[1]
        self.lenses[label] = (focal, position)

    def remove(self, label: str):
        if label in self.lenses:
            del self.lenses[label]

    def __iter__(self) -> Iterable[Tuple[int, int]]:
        return ((slot, focal) for slot, (focal, _) in enumerate(sorted(self.lenses.values(), key=lambda item: item[-1]), 1))


def part2(input_: Iterable[str]) -> int:
    boxes = tuple(Box() for _ in range(256))
    for string in parse_intput(input_):
        label, add = re.match(r'(\w+)(?:-|=(\d+))', string).groups()
        hashed = hash_(label)
        if add:
            boxes[hashed].add(label, int(add))
        else:
            boxes[hashed].remove(label)
    return sum(box_number * sum(slot * focal for slot, focal in box) for box_number, box in enumerate(boxes, 1))


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))
