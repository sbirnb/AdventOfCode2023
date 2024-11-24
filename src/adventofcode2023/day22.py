import re 
from typing import Iterable, Tuple, Set, Sequence, Mapping
import sys
from collections import defaultdict

Brick = Tuple[Tuple[int, int, int], Tuple[int, int, int]]

def parse_input(rows: Iterable[str]) -> Iterable[Brick]:
	return (
		tuple(sorted(((x1, y1, z1), (x2, y2, z2))))
		for x1, y1, z1, x2, y2, z2 in (
			(int(x) for x in re.findall(r'\d+', row)) for row in rows
		)
	)

def cells(brick: Brick) -> Iterable[Tuple[int, int]]:
	((x1, y1, z1), (x2, y2, z2)) = sorted(brick)
	if x1 != x2:
		return ((x, y1, z1) for x in range(x1, x2 + 1))
	elif y1 != y2:
		return ((x1, y, z1) for y in range(y1, y2 + 1))
	else:
		return ((x1, y1, z) for z in range(z1, z2 + 1))


def footprint(brick: Brick) -> Iterable[Tuple[int, int]]:
	((x1, y1, _), (x2, y2, _)) = sorted(brick)
	if x1 == x2:
		return ((x1, y) for y in range(y1, y2 + 1))
	else:
		return ((x, y1) for x in range(x1, x2 + 1))

def set_z(brick: Brick, z: int) -> Brick:
	((x1, y1, z1), (x2, y2, z2)) = brick
	bottom, top = sorted((z1, z2))
	return ((x1, y1, z), (x2, y2, z2 + (z - z1)))

def bottom(brick: Brick) -> int:
	return min(c[2] for c in brick)

def top(brick: Brick) -> int:
	return max(c[2] for c in brick)

def height(brick: Brick) -> int:
	return abs(brick[0][2] - brick[1][2]) + 1

def get_brick_supports(bricks: Iterable[Brick]) -> Iterable[Tuple[int, Tuple[int, ...]]]:
	top_bricks = dict()
	indexes = dict()
	for i, brick in enumerate(bricks):
		supports = set()
		bottom = max((0, *(top(top_bricks[xy]) for xy in footprint(brick) if xy in top_bricks))) + 1
		fallen_brick = set_z(brick, bottom)
		indexes[fallen_brick] = i
		for xy in footprint(fallen_brick):
			if xy in top_bricks and top(top_bricks[xy]) == bottom - 1:
				supports.add(indexes[top_bricks[xy]])
			top_bricks[xy] = fallen_brick
		yield i, (*supports,)


def invert(forward: Mapping[int, Tuple[int, ...]]) -> Mapping[int, Sequence[int]]:
	backwards = defaultdict(list)
	for key, values in forward.items():
		for value in values:
			backwards[value].append(key)
	return backwards

def get_single_supports(supports: Iterable[Tuple[int, Tuple[int, ...]]]) -> Set[int]: 
	return {
		s[0] for i, s in supports if len(s) == 1
	}

def get_falling_bricks(
	first: int, 
	supporting: Mapping[int, Sequence[int]],
	initial_supported_count: Mapping[int, int]
) -> Iterable[int]:
	supported_count = dict(initial_supported_count)
	queue = [first]
	while queue:
		brick = queue.pop()
		for supported in supporting[brick]:	
			supported_count[supported] -= 1
			if supported_count[supported] == 0:
				yield supported 
				queue.append(supported)	


def part1(input_: Iterable[str]) -> int:
	bricks = sorted(parse_input(input_), key=lambda b: min(e[2] for e in b))
	single_supports	= get_single_supports(get_brick_supports(bricks))
	return len(bricks) - len(single_supports)

def part2(input_: Iterable[str]) -> int:
	bricks = sorted(parse_input(input_), key=lambda b: min(e[2] for e in b))
	supports = tuple(get_brick_supports(bricks))
	supported_by = dict(supports)
	supported_by_count = {k: len(v) for k, v in supported_by.items()}
	supporting = invert(supported_by)
	single_supports = get_single_supports(supports)
	total = 0
	for brick in single_supports:
		total += sum(1 for _ in get_falling_bricks(brick, supporting, supported_by_count))
	return total



if __name__ == '__main__':
	#input_ = tuple(sys.stdin)
	with open('../../inputs/day22.txt', 'r') as fi:
		input_ = tuple(fi)
	print(part1(input_))
	print(part2(input_))
