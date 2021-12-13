from typing import List, Iterable
import itertools
from collections import deque

RAW = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


class Grid:
    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.nr = len(self.grid)
        self.nc = len(self.grid[0])
        assert (self.nr == self.nc)

    def get_neighbors(self, i: int, j: int) -> Iterable:
        steps = (-1, 0, 1)
        for dr, dc in itertools.product(steps, steps):
            if dr == 0 and dc == 0: # center at (i, j)
                continue
            if (0 <= i + dr < self.nr) and (0 <= j + dc < self.nc):
                yield (i + dr, j + dc)
    
    def step(self) -> int:
        queue = deque((i, j) for i in range(self.nr) for j in range(self.nc)) 
        flashed = set()
        while queue:
            i, j = queue.popleft()
            # sum 1 if the has not flashed yet
            if (i, j) not in flashed:
                self.grid[i][j] += 1

            # if it reach the top energy
            if self.grid[i][j] > 9:
                # set it to 0 and increase the number of flashes
                flashed.add((i, j))
                self.grid[i][j] = 0
                # add non flashed neighbors to stack
                for ii, jj in self.get_neighbors(i, j):
                    if (ii, jj) not in flashed:
                        queue.append((ii, jj))
        return len(flashed)

    
    def n_flashes_after(self, step: int) -> int:
        return sum(self.step() for _ in range(step))


    def step_until_all_flashes(self) -> int:
        for step in itertools.count(1):
            if (self.step() == self.nr * self.nc):
                return step

    @staticmethod
    def parse(raw: str) -> 'Grid':
        grid = [list(map(int, row)) for row in raw.strip().splitlines()]
        return Grid(grid)


def n_flashes_after_n_steps(raw_string: str, steps: int) -> int:
    grid = Grid.parse(raw_string)
    return grid.n_flashes_after(steps)


def step_until_all_flashes(raw_string: str) -> int:
    grid = Grid.parse(raw_string)
    return grid.step_until_all_flashes()


N_FLASHES = n_flashes_after_n_steps(RAW, steps=100)
assert N_FLASHES == 1656, N_FLASHES

N_STEPS = step_until_all_flashes(RAW)
assert N_STEPS == 195, N_STEPS


if __name__ == '__main__':
    with open('data/input.txt') as f:
        contest_raw = f.read()
    contest_grid = Grid.parse(contest_raw)
    contest_n_flashes = n_flashes_after_n_steps(contest_raw, steps=100)
    print('contest sol part 1')
    print(contest_n_flashes)
    print('contest sol part 2')
    contest_n_steps = step_until_all_flashes(contest_raw)
    print(contest_n_steps)
