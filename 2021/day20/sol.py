from collections import defaultdict
from typing import List, Tuple, Dict, Set
import itertools


Pixels = List[str]
IJ = Tuple[int, int]
Grid = Dict[IJ, bool]
adj_3x3_square = list(itertools.product((-1, 0, 1), repeat=2))


def make_pixel_grid(pixels: Pixels) -> Grid:
    nr = len(pixels)
    nc = len(pixels[0])
    return {(ii, jj): pixels[ii][jj] == '#'
            for ii in range(nr) for jj in range(nc)}


def make_adj_grid(grid: Grid) -> Set[IJ]:
    return {(i + di, j + dj) for i, j in grid for di, dj in adj_3x3_square}


def enhance_image(grid: Grid,
                  rules: str,
                  repeat: int = 2) -> Grid:
    for k in range(repeat):
        # init a new grid, with default (i, j) set to off
        enhance_grid = defaultdict(bool)

        # compute adjacent position
        adj_grid = make_adj_grid(grid)
        # for every position
        for i, j in adj_grid:
            index = 0

            # compute the rule's index 
            for di, dj in adj_3x3_square:
                ii, jj = i + di, j + dj
                # if (ii, jj) in grid, use the stored value
                if (ii, jj) in grid:
                    light_up = grid[(ii, jj)]
                # if the rule[0] is #, the infinity grid will turn on and off
                # every iteration, if the iter number is odd, then the infinity grid
                # will be #
                elif rules[0] == '#':
                    light_up = k % 2
                # otherwise, 0
                else:
                    light_up = 0
                index = 2 * index + light_up
            # add the pos (i, j) to the new grid
            enhance_grid[(i, j)] = rules[index] == '#'
        grid = enhance_grid
    return grid


def count_light_up_pixel(grid: Grid, rules: str, repeat: int) -> int:
    grid = enhance_image(grid, rules, repeat)
    return sum(grid.values())    


def parse_file(file) -> Tuple[Grid, str]:
    with open(file) as f:
        raw = f.read()
    rules, pixels = raw.split('\n\n')
    grid = make_pixel_grid(pixels.splitlines())
    assert len(rules) == 512
    return grid, rules


GRID, RULES = parse_file('data/raw.txt')
test_case_sol1 = count_light_up_pixel(GRID, RULES, repeat=2)
assert test_case_sol1 == 35

test_case_sol2 = count_light_up_pixel(GRID, RULES, repeat=50)
assert test_case_sol2 == 3351

if __name__ == '__main__':
    contest_grid, contest_rules = parse_file('data/input.txt')
    contest_sol1 = count_light_up_pixel(contest_grid, contest_rules, repeat=2)
    print('contest sol part 1')
    print(contest_sol1)

    contest_sol2 = count_light_up_pixel(contest_grid, contest_rules, repeat=50)
    print('contest sol part 2')
    print(contest_sol2)





