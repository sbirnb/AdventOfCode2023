import re
from typing import Tuple, Iterable, Optional
from fractions import Fraction
from itertools import combinations
from functools import reduce


def parse_input(input_: Iterable[str]) -> Iterable[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]:
	return (((int(x), int(y), int(z), int(dx), int(dy), int(dz))) for x, y, z, dx, dy, dz in (re.findall(r'-?\d+', row) for row in input_))


def get_time_in_bounds_1d(x: int, dx: int, lb: int, ub: int) -> Tuple[Fraction, Fraction]:
	if dx != 0:
		return tuple(sorted(
			(max(0, Fraction(lb - x, dx)), max(0, Fraction(ub - x, dx)))
			)
		)
	elif lb <= x <= ub:
		return Fraction(0), Fraction(float(inf))
	else: 
		return Fraction(0), Fraction(-1)


def get_time_in_bounds(xdx: Tuple[Tuple[int, int], ...], lb: int, ub: int) -> Tuple[Fraction, Fraction]:
	return reduce(
		(lambda b0, b1: (max(b0[0], b1[0]), min(b0[1], b1[1]))), 
		(get_time_in_bounds_1d(x, dx, lb, ub) for x, dx in xdx)
	)



def rref(matrix: Tuple[Tuple[Fraction, ...], ...]) -> Tuple[Tuple[Fraction, ...]]:
	augmented = list(matrix)
	for pivot in range(len(matrix)):
		max_index, pivot_row = max(enumerate(augmented[pivot:], pivot), key=lambda i_r: abs(i_r[1][pivot]))
		if pivot_row[pivot] == 0:
			break
		augmented[max_index], augmented[pivot] = augmented[pivot], (lambda r: (lambda k: tuple(k * v for v in r))(1/r[pivot]))(augmented[max_index])
		augmented[pivot + 1:] = (tuple(v1 - r[pivot] * v2 for v1, v2 in zip(r, augmented[pivot])) for r in augmented[pivot + 1:])
	for i in range(pivot, 0, -1):
		row = augmented[i]
		augmented[:i] = (tuple(v1 - r[i] * v2 for v1, v2 in zip(r, row)) for r in augmented[:i])
	return tuple(augmented)


def eval_at(x: Tuple[Fraction, ...], d: Tuple[Fraction, ...], t: Fraction) -> Tuple[Fraction, ...]:
	return tuple(xi + t * di for xi, di in zip(x, d))



def intersects_in_range(
	xdxb: Tuple[Tuple[int, int], Tuple[int, int], Tuple[Fraction, Fraction]],
	ydyb: Tuple[Tuple[int, int], Tuple[int, int], Tuple[Fraction, Fraction]]
):
	(x1, x2), (dx1, dx2), (t_lb, t_ub) = x, dx, _ = xdxb
	(y1, y2), (dy1, dy2), (u_lb, u_ub) = y, dy, _ = ydyb
	(a, _, t), (_, b, u) = rref(((Fraction(dx1), Fraction(-dy1), Fraction(y1 - x1)), (Fraction(dx2), Fraction(-dy2), Fraction(y2 - x2))))
	if b != 0:
		return t_lb <= t and t <= t_ub and u_lb <= u and u <= u_ub
	elif u != 0:
		return False

	p0, p1 = sorted(eval_at(x, dx, ti) for ti in t)
	q0, q1 = sorted(eval_at(y, dy, ui) for ui in u)

	intersects = max(p0[0], q0[0]) <= min(p1[0], q1[0])  \
		and max(p0[1], q0[1]) <= min(p1[1], q1[1])
	print(intersects)
	return intersects


def cross(x1: Tuple[int, int, int], x2: Tuple[int, int, int]) -> Tuple[int, int, int]:
	a1, a2, a3 = x1 
	b1, b2, b3 = x2
	return (
		a2 * b3 - a3 * b2,
		a3 * b1 - a1 * b3,
		a1 * b2 - a2 * b1
	)

def dot(x1: Tuple[int, ...], x2: Tuple[int, ...]) -> int:
	return sum(a * b for a, b in zip(x1, x2))

def sub(x1: Tuple[int, ...], x2: Tuple[int, ...]) -> Tuple[int, ...]:
	return tuple(a - b for a, b in zip(x1, x2))

def part1(input_: Iterable[str]):
	vecs = tuple(((x, y), (dx, dy), get_time_in_bounds(((x, dx), (y, dy)), 200000000000000, 400000000000000)) for x, y, _, dx, dy, _ in parse_input(input_))
	return sum(intersects_in_range(v1, v2) for v1, v2 in combinations(vecs, 2))


def part2(input_: Iterable[str]) -> int:
	vecs = tuple(
		(tuple(r[:3]), tuple(r[3:])) for r in parse_input(input_)
	)
	(p0, d0), others = vecs[0], vecs[1:]
	shifted = tuple(
		(sub(p1, p0), sub(d1, d0)) for p1, d1 in others
	)
	(p1, d1), others_shifted = shifted[0], shifted[1:]
	collision_times = tuple(
		Fraction(-dot(cross(pi, p1), d1), dot(cross(di, p1), d1)) for pi, di in others_shifted
	)
	collisions = tuple(
		tuple(x0 + xi + (dx0 + dxi) * t for x0, dx0, xi, dxi in zip(p0, d0, p, d)) for (p, d), t in zip(others_shifted, collision_times)
	)

	(q2, q3) = collisions[:2]
	t2, t3 = collision_times[:2]
	dt = t2 - t3
	d = tuple((x2 - x3) / dt for x2, x3 in zip(q2, q3))
	x = tuple(x2 - t2 * di for x2, di in zip(q2, d))
	return sum(x2 - t2 * di for x2, di in zip(q2, d))



if __name__ == '__main__':
	with open('../../inputs/day24.txt', 'r') as fi:
		input_ = tuple(fi)

	print(part1(input_))
	print(part2(input_))



