from typing import NamedTuple, List


class SubCommand(NamedTuple):
    horizontal: int
    depth: int

    @classmethod
    def from_raw(cls, command_str: str):
        command, unit = command_str.split(' ')
        unit = int(unit)
        horizontal = 0
        depth = 0
        if command == 'forward':
            horizontal += unit
        elif command == 'down':
            depth += unit
        else:
            depth -= unit
        return cls(horizontal, depth)


def compute_position(commands: List[SubCommand]) -> int:
    horizontal, depth = 0, 0

    for c in commands:
        horizontal += c.horizontal
        depth += c.depth
    return  horizontal * depth
        

RAW = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""

if __name__ == '__main__':
    INPUT = [SubCommand.from_raw(x) for x in RAW.strip().split('\n')]

    test_case_sol1 =  compute_position(INPUT)
    print('test case sol part 1')
    print(test_case_sol1)
    assert test_case_sol1 == 150


    with open('data/input.txt') as f:
        raw = f.read()
    contest_input = [SubCommand.from_raw(x) for x in raw.strip().split('\n')]

    output = compute_position(contest_input)
    print('contest sol part 1')
    print(output)