from typing import Iterable, Mapping, Sequence, Tuple, Optional	
import heapq
from mip import Model, xsum, maximize, BINARY, INTEGER
from collections import defaultdict

def parse_input(input_: Iterable[str], include_slopes: bool) -> Mapping[int, Sequence[int]]:
	maze = tuple(row.strip() for row in input_)

	def adjacent(row: int, col: int, include_slopes1: bool = True) -> Iterable[Tuple[int, int]]:
		
		def checking_slope(slope: str) -> str:
			return '#' + slope if include_slopes1 else '#'

		if row > 0 and maze[row - 1][col] not in checking_slope('v'):
			yield row - 1, col
		if row < len(maze) - 1 and maze[row + 1][col] not in checking_slope('^'):
			yield row + 1, col
		if col > 0 and maze[row][col - 1] not in checking_slope('>'):
			yield row, col - 1
		if col < len(maze[0]) - 1 and maze[row][col + 1] not in checking_slope('<'):
			yield row, col + 1

	def next_steps(last: Tuple[int, int], current: Tuple[int, int]) -> Iterable[Tuple[int, int]]:
		return (step for step in adjacent(*current, include_slopes) if step != last)

	def is_node(row: int, col: int) -> bool:
		return row == 0 \
				or row == len(maze) - 1 \
				or col == 0 or col == len(maze[0]) - 1 \
				or sum(1 for _ in adjacent(row, col, False)) > 2

	def find_next_node(node: Tuple[int, int], direction: Tuple[int, int]) -> Optional[Tuple[int, Tuple[int, int]]]:
		last = node
		current = direction
		weight = 1
		while not is_node(*current):
			weight += 1
			try:
				last, current = current, next(adj for adj in adjacent(*current, include_slopes) if adj != last)
			except StopIteration:
				return None
		return weight, current

	def find_next_nodes(node: Tuple[int, int]) -> Iterable[Tuple[int, Tuple[int, int]]]:
		return (
			next_node for adj in adjacent(*node, include_slopes)
			if (next_node := find_next_node(node, adj))
		)

	queue = [(0, 1)]
	next_nodes = dict()

	while queue:
		node = queue.pop()
		next_nodes[node] = tuple(find_next_nodes(node))
		queue.extend(set(node for _, node in next_nodes[node]) - next_nodes.keys())

	return next_nodes 


def part1(input_: Iterable[str]) -> int:
	node_map = parse_input(input_, True)
	queue = [(0, set(), (0, 1))]
	longest = (0, set(), (0, 1))
	while queue:
		weight, visited, tail = heapq.heappop(queue)
		for w, node in node_map[tail]:
			if node in visited:
				continue
			x = (weight - w, visited | {tail}, node)
			longest = min(longest, x)
			heapq.heappush(queue, x)
	return -longest[0]


def part2(input_: Iterable[str]) -> int:
	node_map = tuple(parse_input(input_, False).items())
	origin = (0, 1)
	destination = max(node for node, _ in node_map)

	m = Model()

	edge_set = defaultdict(lambda : m.add_var(var_type=BINARY))
	node_set = defaultdict(lambda : m.add_var(var_type=BINARY))
	node_ord = defaultdict(lambda : m.add_var(var_type=INTEGER))
	m.objective = maximize(xsum(edge_set[source, target] * weight for source, targets in node_map for weight, target in targets if source != destination and target != origin))

	m.add_constr(node_set[origin] == 1)
	m.add_constr(node_set[destination] == 1)
	m.add_constr(node_ord[origin] == 0)
	for node, adjs in node_map:
		if node != origin:
			m.add_constr(xsum(edge_set[source, node] for _, source in adjs if source != destination) - node_set[node] == 0)
			m.add_constr(node_ord[node] >= 0)
			m.add_constr(node_ord[node] <= len(node_map) - 1)
			for _, source in adjs:
				if source != destination:
					m.add_constr(node_ord[node] >= node_set[node] + node_ord[source] + edge_set[source, node] * len(node_map) - len(node_map))
		if node != destination:
			m.add_constr(xsum(edge_set[node, target] for _, target in adjs if target != origin) - node_set[node] == 0)

	m.verbose = 0
	m.optimize()
	return m.objective_value


if __name__ == '__main__':
	with open('../../inputs/day23.txt', 'r') as fi:
		input_ = tuple(fi)
	print(part1(input_))
	print(part2(input_))
