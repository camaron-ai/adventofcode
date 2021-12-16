from typing import List, Iterable, Tuple
from collections import deque, defaultdict

XY = Tuple[int, int]
RAW = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

class Grid:
    def __init__(self, grid: List[List[int]], expand_dim: int = 1):
        self.grid = grid
        self.expand_dim = expand_dim
        assert len(self.grid) == len(self.grid[0])
        self.size = len(self.grid)
    
    def __len__(self) -> int:
        return self.expand_dim * self.size
    
    def __getitem__(self, pos: XY) -> int:
        i, j = pos
        # actual grid value
        ii = i % self.size
        jj = j % self.size
        # risk value
        risk = self.grid[ii][jj]

        i_offset = i // self.size
        j_offset = j // self.size
    
        if i_offset == 0 and j_offset == 0:
            return risk

        risk = (risk + i_offset + j_offset)
        if risk > 9:
            risk = risk + 1
        return risk % 10
    
    def get_neighbors(self, i: int, j: int) -> Iterable[XY]:
        # neightbors
        # [down, right, left, up]
        for ii, jj in [(i, j-1), (i+1, j), (i-1, j), (i, j+1)]:
            if 0 <= ii < len(self) and 0 <= jj < len(self):
                yield (ii, jj)

    @staticmethod
    def parse(raw_string: str, expand_dim: int = 1) -> 'Grid':
        lines = raw_string.strip().splitlines()
        return Grid([[int(x) for x in row] for row in lines], expand_dim)


def find_lowest_risk_path(grid: Grid,
                          start=(0, 0),
                          ) -> int:
    size = len(grid) - 1
    memo = defaultdict(lambda: float('inf'))
    memo[start] = 0
    queue = deque([start])

    while queue:
        i, j = queue.popleft()
        for ii, jj in grid.get_neighbors(i, j):
            new_risk_level = memo[(i, j)] + grid[(ii, jj)]
            if new_risk_level < memo[(ii, jj)]:
                memo[(ii, jj)] = new_risk_level
                queue.append((ii, jj))

    return memo[(size, size)]


GRID = Grid.parse(RAW)
test_case_sol1 = find_lowest_risk_path(GRID)
assert test_case_sol1 == 40


GRID_5X5 = Grid.parse(RAW, expand_dim=5)
test_case_sol2 = find_lowest_risk_path(GRID_5X5)
test_case_sol2 == 315


if __name__ == '__main__':
    with  open('data/input.txt') as f:
        raw_contest = f.read()

    contest_grid = Grid.parse(raw_contest)
    contest_sol1 = find_lowest_risk_path(contest_grid)
    print('contest sol part 1')
    print(contest_sol1)
    contest_sol1 == 656

    contest_grid_5x5 = Grid.parse(raw_contest, expand_dim=5)
    contest_sol2 = find_lowest_risk_path(contest_grid_5x5)
    print('contest sol part 2')
    print(contest_sol2)
    assert contest_sol2 == 2979
