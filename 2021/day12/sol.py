from typing import Iterable, Dict, List, Set, Callable
from collections import defaultdict, Counter, deque


RAW = ["""start-A
start-b
A-c
A-b
b-d
A-end
b-end""",
"""dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""",
"""fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""
]

expected_sol1 = [10, 19, 226]
expected_sol2 = [36, 103, 3509]


def build_cave_map(raw_string: str) -> Dict[str, List[str]]:
    caves = defaultdict(list)
    for line in raw_string.strip().splitlines():
        start, end = line.split('-')
        caves[start].append(end)
        caves[end].append(start)
    return caves


def is_big_cave(cave: str) -> bool:
    return cave.isupper() 


def is_node_allowed(next_cave: str, visited: Set[int], visited_twice) -> bool:
    return is_big_cave(next_cave) or (next_cave not in visited) or (not visited_twice)


def find_all_paths(caves: Dict[str, List[str]],
                   start: str = 'start',
                   end: str = 'end',
                   allow_visit_twice: bool = False) -> int:

        
    # init a queue with the last_visited_cave, cave visited and
    # if the path has visited a small cave twice
    paths = deque([
        [(start, set(), not allow_visit_twice)]
    ])

    total_path_count = 0

    while paths:
        path = paths.popleft()
        last_visited_cave, visited, visited_twice = path[-1]
        if last_visited_cave == end:
            total_path_count += 1
        else:
            for next_cave in caves[last_visited_cave]:
                if is_node_allowed(next_cave, visited, visited_twice) and (next_cave != start):
                    has_visited_twice = (True if (next_cave in visited) and (not is_big_cave(next_cave))
                                        else visited_twice)
                    paths.append(path + [(next_cave, visited | {next_cave}, has_visited_twice)])
    return total_path_count


for i, raw_string in enumerate(RAW):
    CAVES = build_cave_map(raw_string)
    max_n_paths = find_all_paths(CAVES, allow_visit_twice=False)
    assert max_n_paths == expected_sol1[i], max_n_paths
    max_n_paths_twice = find_all_paths(CAVES, allow_visit_twice=True)
    assert max_n_paths_twice == expected_sol2[i], max_n_paths_twice


if __name__ == '__main__':
    with open('data/input.txt') as f:
        contest_raw = f.read()
    contest_map = build_cave_map(contest_raw)
    contest_max_n_paths = find_all_paths(contest_map)
    print(contest_max_n_paths)

    assert contest_max_n_paths == 4749
    contest_twice_max_n_paths = find_all_paths(contest_map, allow_visit_twice=True)
    print(contest_twice_max_n_paths)
    assert contest_twice_max_n_paths == 123054
