from collections import defaultdict
from typing import NamedTuple, List

RAW = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


class Line(NamedTuple):
    x1: int
    y1: int
    x2: int
    y2: int

    @staticmethod
    def parse(string: str) -> 'Line':
        start, end = string.split(' -> ')
        x1, y1 = map(int, start.split(','))
        x2, y2 = map(int, end.split(','))
        return Line(x1=x1, y1=y1, x2=x2, y2=y2)

    def is_flat(self) -> bool:
        return (self.x1 == self.x2) or (self.y1 == self.y2)

    def compute_line_corrs(self):
        if self.is_flat():
            return self.flat_line_corrs()
        else:
            return self.diag_line_corrs()
    
    def flat_line_corrs(self):
        lx = min(self.x1, self.x2)
        hx = max(self.x1, self.x2)
        ly = min(self.y1, self.y2)
        hy = max(self.y1, self.y2)
        for x in range(lx, hx + 1):
            for y in range(ly, hy + 1):
                yield x, y

    def diag_line_corrs(self):
        dx = 1 if (self.x2 >= self.x1) else -1
        dy = 1 if (self.y2 >= self.y1) else -1 

        x_range = range(self.x1, self.x2 + dx, dx)
        y_range = range(self.y1, self.y2 + dy, dy)
        for x_step, y_step in zip(x_range, y_range):
            yield x_step, y_step


def compute_grid_score(lines: List[Line], only_flat_lines: bool = True):
    grid = defaultdict(lambda: 0)
    for line in lines:
        if only_flat_lines and (not line.is_flat()):
            continue

        for corr in line.compute_line_corrs():
            grid[corr] += 1
    return sum(count >= 2 for count in grid.values())


if __name__ == '__main__':
    TEST_CASE_INPUT = RAW.splitlines()
    LINES = [Line.parse(x) for x in TEST_CASE_INPUT]

    test_case_sol1 = compute_grid_score(LINES, only_flat_lines=True)
    print('test case sol part 1')
    print(test_case_sol1)
    assert test_case_sol1 == 5, test_case_sol1

    print('test case sol part 2')
    test_case_sol2 = compute_grid_score(LINES, only_flat_lines=False)
    print(test_case_sol2)
    assert test_case_sol2 == 12

    with open('data/input.txt') as f:
        CONTEST_RAW = f.read()

    CONTEST_LINES = [Line.parse(x)
                     for x in CONTEST_RAW.splitlines()]

    contest_sol_par1 = compute_grid_score(CONTEST_LINES, only_flat_lines=True)
    print('contest sol par 1')
    print(contest_sol_par1)
    
    # assert contest_sol_par1 == 6005 
    contest_sol_par2 = compute_grid_score(CONTEST_LINES, only_flat_lines=False)
    print('contest sol par 2')
    print(contest_sol_par2)
    assert contest_sol_par2 == 23864
    
