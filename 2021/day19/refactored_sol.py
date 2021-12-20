from typing import List, Optional, Tuple, Iterable
import itertools
from collections import deque
import math


XYZ = Tuple[int, int, int]
Orientation = List[int]
Axis = List[int]
AT_LEAST = 12


def get_axis_rotatation() -> Iterable[XYZ]:
    yield from itertools.permutations((0, 1, 2))

def get_orientation() -> Iterable[XYZ]:
    yield from itertools.product((1, -1), (1, -1), (1, -1))


def compute_distance(p1: XYZ, p2: XYZ) -> float:
    assert len(p1) == len(p2)
    return math.sqrt(sum((p1[axis] - p2[axis])**2 for axis in range(len(p1))))



class Scanner:
    def __init__(self, points: List[XYZ], location: Optional[XYZ] = None) -> None:
        self.points = points
        self.location = location if location else [0, 0, 0]
        self.compute_distances()

    def compute_distances(self):
        self.distances = [
            sorted([compute_distance(p1, p2)
             for i, p1 in enumerate(self.points) if i != j])
             for j, p2 in enumerate(self.points)]

    def rotate(self, axis: XYZ, orientation: XYZ) -> 'Scanner':
        rotated_points = []
        for point in self.points:
            rotated_point = [0, 0, 0]
            for index, value in enumerate(point):
                new_value = value * orientation[index]
                rotated_point[axis[index]] = new_value
            rotated_points.append(rotated_point)
        return Scanner(rotated_points, self.location)


    def find_location(self, center: 'Scanner', at_least: int = 12) -> Optional['Scanner']:

        common_points = {}
        # iter through the distances list and find common distances
        for i, center_distances in enumerate(center.distances):
            for j, distances in enumerate(self.distances):
                common_distances = sum(center_distances[k] == distances[k]
                                        for k in range(at_least))
                if common_distances > 1:
                    common_points[i] = j
                    break
    
        # no overlapping points
        if (len(common_points) < 1):
            return None
        

        location = [None, None, None]
        axis = [None, None, None]
        orientation = [None, None, None]

        # for each axis
        for current_axis in range(3):
            # for each possible orientation
            for sign in (1, -1):
                perm_locations = [[], [], []]
                # for each common point
                for center_point_id, point_id in common_points.items():
                    center_point = center.points[center_point_id]
                    point = self.points[point_id]

                    # compute the axis location relative to the center point
                    # if the axis and location, all 3 location must be equal
                    perm_locations[0].append(center_point[0] - sign * point[current_axis])
                    perm_locations[1].append(center_point[1] - sign * point[current_axis])
                    perm_locations[2].append(center_point[2] - sign * point[current_axis])
    
                # if all location match, we found the right orientation and axis
                for center_axis, axis_locations in enumerate(perm_locations):
                    if len(set(axis_locations)) == 1:
                        location[center_axis] = axis_locations[0]
                        axis[current_axis] = center_axis
                        orientation[current_axis] = sign


        # if all location are not determined, return None
        if any(x is None for x in location):
            return None

        assert len(set(location)) == 3
        scanner = self.rotate(axis, orientation)
        relative_location = [center.location[axis] + location[axis] for axis in range(3)]
        scanner.location = relative_location
        return scanner
    
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
    

def find_all_location(scanners: List['Scanner']) -> List['Scanner']:
    seen = {0}
    queue = deque([0])
    while queue:
        center_id = queue.popleft()
        center = scanners[center_id]
        for scanner_id, scanner in enumerate(scanners):
            if scanner_id not in seen:
                relative_scanner = scanner.find_location(center, at_least=AT_LEAST)
                if relative_scanner:
                    scanners[scanner_id] = relative_scanner
                    queue.append(scanner_id)
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

EXPECTED_LOC = [
    [0, 0, 0],
    [ 68, -1246, -43],
    [1105, -1205, 1229],
    [-92, -2380, -20],
    [-20, -1133, 1061]
            ]
            

SCANNERS = parse_file('data/raw.txt')
SCANNERS = find_all_location(SCANNERS)

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