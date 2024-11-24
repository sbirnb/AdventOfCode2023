from typing import Mapping, Iterable, Collection, Set, Sequence, Optional
import re
from collections import defaultdict

def parse_input(input_: Iterable[str]) -> Mapping[str, Collection[str]]:
	graph = defaultdict(set)
	for row in input_:
		(source, *targets) = re.findall(r'\w+', row)
		for target in targets:
			graph[source].add(target)
			graph[target].add(source)
	return graph


def find_path(graph: Mapping[str, Collection[str]], cluster: Collection[str], target: str, exclude_edges: Collection[Set[str]]) -> Optional[Sequence[str]]:
	queue = [(target,)]
	visited = {target}
	while queue:
		path = queue.pop(0)
		tail = path[-1]
		for adjacent in (node for node in graph[tail] if {node, tail} not in exclude_edges and node not in visited):
			visited.add(adjacent)
			if adjacent in cluster:
				return (*path, adjacent)
			queue.append((*path, adjacent))
	return None

def choose_candidate(graph: Mapping[str, Collection[str]], cluster: Collection[str], exclude: Collection[str]) -> Optional[str]:
	boundary_edges = defaultdict(set)
	for node in cluster:
		for adjacent in graph[node]:
			if adjacent not in cluster and adjacent not in exclude:
				boundary_edges[adjacent].add(node)
	if not boundary_edges:
		return None
	return max(boundary_edges, key = lambda node: len(boundary_edges[node]))


def part1(input_: Iterable[str]) -> int:
	graph = parse_input(input_)
	cluster = {next(iter(graph))}
	other_cluster = set()
	cut_edges = set()

	while True:
		target = choose_candidate(graph, cluster, other_cluster)
		if not target:
			return len(cluster) * (len(graph) - len(cluster))
		exclude_edges = set()
		paths = []
		for _ in range(4):
			path = find_path(graph, cluster, target, exclude_edges)
			if path:
				paths.append(path)
				exclude_edges.update(frozenset((node1, node2)) for node1, node2 in zip(path, path[1:]))
			else: 
				other_cluster.add(target)
				break
		else:
			cluster.add(target)
	return None
		

if __name__ == '__main__':
	with open('../../inputs/day25.txt', 'r') as fi:
		input_ = tuple(fi)

	print(part1(input_))
