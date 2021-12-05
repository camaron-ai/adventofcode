from typing import List
import itertools

RAW = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""

class Board:
    def __init__(self, board: List[int]):
        self.marked_rows = [0 for _ in range(5)]
        self.marked_cols = [0 for _ in range(5)]
        self.board = board
        self.total_sum = sum(board)

    def mark(self, n: int):
        try:
            index = self.board.index(n)
            row = index // 5
            col = index % 5

            self.marked_rows[row] += 1
            self.marked_cols[col] += 1

            self.total_sum -= n
        except ValueError:
            pass

    def bingo_score(self) -> int:
        for count in itertools.chain(self.marked_rows, self.marked_cols):
            if count == 5:
                return self.total_sum
        return -1
        

def parse_input(string: str):
    lines = string.strip().split('\n\n')
    numbers, *grids = lines
    numbers = [int(x) for x in numbers.strip().split(',')]
    
    boards = [
                Board([int(x) for row in grid.split('\n')
                 for x in row.split()])
              for grid in grids
            ]
    return numbers, boards


def compute_bingo_score(numbers: List[int],
                        boards: List[Board]) -> int:
    for n in numbers:
        for board in boards:
            board.mark(n)
            bingo_score = board.bingo_score()
            if bingo_score >= 0:
                return n * bingo_score
    raise ValueError('No winner!')

def compute_last_bingo_score(numbers: List[int],
                             boards: List[Board]) -> int:

    last = None

    for n in numbers:
        to_drop = []
        if len(boards) == 0:
            break

        for board_idx, board in enumerate(boards):
            board.mark(n)
            bingo_score = board.bingo_score()
            if bingo_score >= 0 and len(boards) == 1:
                return n * bingo_score
            elif bingo_score >= 0:
                to_drop.append(board_idx)

        for i, board_idx in enumerate(to_drop):
            boards.pop(board_idx - i)

    if last is None:
        raise ValueError('No winner!')
    return last[0] * last[1]


if __name__ == '__main__':
    numbers, boards = parse_input(RAW)
    test_case_bingo_score = compute_bingo_score(numbers, boards)
    print('test case sol part 1')
    print(test_case_bingo_score)
    assert test_case_bingo_score == 4512

    print('test case sol part 2')
    test_case_bingo_score = compute_bingo_score(numbers, boards)
    numbers, boards = parse_input(RAW)
    test_case_sol2 = compute_last_bingo_score(numbers, boards)
    print(test_case_sol2)
    assert test_case_sol2 == 1924

    with open('data/input.txt') as f:
        test_raw = f.read()

    test_numbers, test_boards = parse_input(test_raw)
    sol1_test_output = compute_bingo_score(test_numbers, test_boards)
    print('contest sol part 1')
    print(sol1_test_output)

    test_numbers, test_boards = parse_input(test_raw)
    sol2_test_output = compute_last_bingo_score(test_numbers, test_boards)
    print('contest sol part 2')
    print(sol2_test_output)


         