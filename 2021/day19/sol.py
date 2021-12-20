from dataclasses import dataclass, field
from typing import List, Optional, NamedTuple, Tuple, Set, Iterable
import itertools
from collections import Counter


XYZ = Tuple[int, int, int]
Orientation = List[int]
Axis = List[int]
AT_LEAST = 12

def get_axis_rotatation() -> Iterable[XYZ]:
    yield from itertools.permutations((0, 1, 2))

def get_orientation() -> Iterable[XYZ]:
    yield from itertools.product((1, -1), (1, -1), (1, -1))


class Scanner:
    def __init__(self, points: List[XYZ], location: Optional[XYZ] = None) -> None:
        self.points = points
        self.location = location if location else [0, 0, 0]
    
    def rotate(self, axis: XYZ, orientation: XYZ) -> 'Scanner':
        rotated_points = []
        for point in self.points:
            rotated_point = [0, 0, 0]
            for index, value in enumerate(point):
                new_value = value * orientation[index]
                rotated_point[axis[index]] = new_value
            rotated_points.append(rotated_point)
        return Scanner(rotated_points, self.location)

    
    def get_all_rotation(self) -> Iterable['Scanner']:
        for axis in get_axis_rotatation():
            for orientation in get_orientation():
                yield self.rotate(axis, orientation)
    
    @staticmethod
    def parse(raw_string: str) -> 'Scanner':
        _, *raw_measurements = raw_string.splitlines()
        measurements = [[int(x) for x in row.split(',')] for row in raw_measurements]
        return Scanner(measurements)
    

def parse_file(file: str) -> List['Scanner']:
    with open(file) as f:
        raw = f.read()
    
    scanners = [Scanner.parse(scanner) for scanner in raw.split('\n\n')]

    return scanners
    

def find_scanner_location_given_rotation(center: Scanner, scanner: Scanner, at_least: int) -> Optional[XYZ]:
    """center scanner is supoosed to be center at (0, 0, 0),
    find the location of the scanner (if possible) given the common points"""

    counter = Counter()

    for target_point in center.points:
        for point in scanner.points:
            location = tuple([target_point[axis] - point[axis]
                              for axis in range(len(target_point))])
            counter[location] += 1
    
    most_common, *_ = counter.most_common(1)
    (location, top_count) = most_common
    if top_count >= at_least:
            return location
    return None


def find_scanner_location(center: Scanner, scanner: Scanner, at_least: int) -> Optional['Scanner']:
    for rotated_scanner in scanner.get_all_rotation():
        location = find_scanner_location_given_rotation(center, rotated_scanner, at_least)
        if location:
            relative_location = [center.location[axis] + location[axis] for axis in range(3)]
            rotated_scanner.location = relative_location
            return rotated_scanner
    return None


def find_all_location(scanners: List['Scanner']) -> List['Scanner']:
    seen = {0}
    stack = [0]

    while stack:
        center_id = stack.pop()
        center = scanners[center_id]
        for scanner_id, scanner in enumerate(scanners):
            if scanner_id not in seen:
                relative_scanner = find_scanner_location(center, scanner, at_least=AT_LEAST)
                if relative_scanner:
                    scanners[scanner_id] = relative_scanner
                    stack.append(scanner_id)
                    seen.add(scanner_id)
    
    return scanners


def find_unique_points(scanners: List['Scanner']) -> int:
    points = [tuple(scan.location[axis] + point[axis] for axis in range(len(point)))
              for scan in scanners
              for point in scan.points]

    return len(set(points))


def compute_manhattan_distance(p1: XYZ, p2: XYZ) -> int:
    assert len(p1) == len(p2)
    return sum(abs(p1[axis] - p2[axis]) for axis in range(len(p1)))

def compute_max_manhattan_distances(scanners: List['Scanner']):
    return max(compute_manhattan_distance(p1.location, p2.location)
              for p1 in scanners for p2 in scanners)



SCANNERS = parse_file('data/raw.txt')
SCANNERS = find_all_location(SCANNERS)

EXPECTED_LOC = [
    [0, 0, 0],
    [ 68, -1246, -43],
    [1105, -1205, 1229],
    [-92, -2380, -20],
    [-20, -1133, 1061]
            ]

for i, scanner in enumerate(SCANNERS):
    assert scanner.location == EXPECTED_LOC[i]

test_case_sol1 = find_unique_points(SCANNERS)
assert test_case_sol1 == 79

test_case_sol2 = compute_max_manhattan_distances(SCANNERS)

assert test_case_sol2 == 3621


if __name__ == '__main__':
    contest_scanners = parse_file('data/input.txt')
    contest_scanners = find_all_location(contest_scanners)

    contest_sol_part1 = find_unique_points(contest_scanners)
    print('contest sol part 1')
    print(contest_sol_part1)

    contest_sol_part2 = compute_max_manhattan_distances(contest_scanners)
    print('contest sol part 2')
    print(contest_sol_part2)