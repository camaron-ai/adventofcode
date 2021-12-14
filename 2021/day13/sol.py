from dataclasses import dataclass
from typing import Tuple, List, NamedTuple, Set

RAW = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""


class Instruction(NamedTuple):
    float_at: int
    axis: int

    @staticmethod
    def parse(raw_string: str) -> 'Instruction':
        raw_string = raw_string[11:]
        axis, float_at = raw_string.split('=')
        axis = (0 if axis == 'x' else 1) 

        return Instruction(axis=axis,
                           float_at=int(float_at))


@dataclass
class Paper:
    dots: Set[Tuple[int, int]]
    instructions: List[Instruction]

    def get_n_dots(self) -> int:
        return len(self.dots)

    def __str__(self) -> str:
        nc = max(i for i, _ in self.dots)
        nr = max(j for _, j in self.dots)

        s = [['#' if (x, y) in self.dots else ' ' for x in range(nc + 1)]
              for y in range(nr + 1)]
        return '\n'.join(''.join(row) for row in s)

    def compute_new_xy_pair(self, x: int, y: int, axis: int, float_at: int):
        updated_value = y if axis == 1 else x
        updated_value = (2 * float_at - updated_value
                         if updated_value > float_at else updated_value)
        if axis == 0:
            return (updated_value, y)
        elif axis == 1:
            return (x, updated_value)

    def fold_paper(self, ins: Instruction) -> 'Paper':
        self.dots = set(self.compute_new_xy_pair(x, y, ins.axis, ins.float_at)
                           for x, y in self.dots)
        return self

    def follow_instruction(self, n: int = None) -> 'Paper':
        if n is None:
            n = len(self.instructions)
        for i in range(n):
            self.fold_paper(self.instructions[i])
        self.instructions = self.instructions[i+1:]
        return self
    
    @staticmethod
    def parse(raw_string: str) -> 'Paper':
        dot_lines, instructions = raw_string.split('\n\n')

        dots = set(tuple(map(int, dot.strip().split(',')))
                    for dot in dot_lines.splitlines())
        
        instructions = [Instruction.parse(raw) for raw in instructions.splitlines()]
        return Paper(dots, instructions)
    


expected_sol1 = [17, 16]
PAPER = Paper.parse(RAW)

for i in range(2):
    PAPER.follow_instruction(1)
    assert PAPER.get_n_dots() == expected_sol1[i], (expected_sol1[i], PAPER.get_n_dots())


if __name__ == '__main__':
    with open('data/input.txt') as f:
        raw_contest = f.read()
    
    contest_paper = Paper.parse(raw_contest)

    contest_paper = contest_paper.follow_instruction(1)
    print('contest sol part 1')
    print(contest_paper.get_n_dots())
    print('contest sol part 2')
    contest_paper = Paper.parse(raw_contest)
    contest_paper = contest_paper.follow_instruction()
    print(contest_paper)