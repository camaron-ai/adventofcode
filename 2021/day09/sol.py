from typing import List, Tuple
import math

RAW = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""


class Heightmap:
    def __init__(self, raw: str):
        self.map = [list(map(int, row))
                    for row in raw.strip().splitlines()]

        self.nrows = len(self.map)
        self.ncols = len(self.map[0])
    
    def get_adjacent_points(self, i: int, j: int) -> int:
        for x, y in [(i, j-1), (i, j+1), (i+1, j), (i-1, j)]:
            if (0 <= x < self.nrows) and (0 <= y < self.ncols):
                yield (x, y)


    def is_lower_point(self, i: int, j: int) -> bool:
        return self.map[i][j] < min(self.map[x][y] for x, y in self.get_adjacent_points(i, j))

    def compute_sum_risk_levels(self) -> int:
        return sum(
            self.map[i][j] + 1
            for i in range(self.nrows)
            for j in range(self.ncols)
            if self.is_lower_point(i, j)
        )
    
    def find_basin_size(self, i: int, j: int) -> int:
        stack = [(i, j)]
        visited = {(i, j)}
        size = 0
        while stack:
            i, j = stack.pop()
            for x, y in self.get_adjacent_points(i, j):
                if self.map[x][y] != 9 and (x, y) not in visited:
                    stack.append((x, y))
                    visited.add((x, y))
            size += 1
        return size
    

    def all_lower_points(self) -> List[Tuple[int, int]]:
        return [(i, j)
                for i in range(self.nrows)
                for j in range(self.ncols)
                if self.is_lower_point(i, j)]


    def all_basin_sizes(self) -> List[int]:
        return [self.find_basin_size(i, j)
                for i, j in self.all_lower_points()]

    def three_largest_basin_product(self) -> int:
        basin_sizes = sorted(self.all_basin_sizes(), reverse=True)
        return math.prod(basin_sizes[:3])







HEIGHTMAP = Heightmap(RAW)
test_case_sol1 = HEIGHTMAP.compute_sum_risk_levels()
assert test_case_sol1 == 15, test_case_sol1

test_case_sol2 = HEIGHTMAP.three_largest_basin_product()
assert test_case_sol2 == 1134



if __name__ == '__main__':
    with open('data/input.txt') as f:
        contest_raw = f.read()
    
    contest_heightmap = Heightmap(contest_raw)

    contest_sol_par1 = contest_heightmap.compute_sum_risk_levels()
    print(contest_sol_par1)

    contest_sol_par2 = contest_heightmap.three_largest_basin_product()
    print(contest_sol_par2)

