from typing import List, Optional, Tuple
import functools


RAW = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


OPEN_CLOSE_MAPPER = {'(': ')', '[': ']', '{': '}', '<': '>'}

SYNTAX_POINT = {
')': 3,
']': 57,
'}': 1197,
'>': 25137,
}

AUTOCOMPLETE_POINT = {
')': 1,
']': 2,
'}': 3,
'>': 4,
}


def get_first_corrupted_bracket(line: str) -> Optional[str]:
    stack = []
    for ch in line:
        # if open bracket, append to the end of the stack
        if ch in OPEN_CLOSE_MAPPER:
            stack.append(ch)
        else:
            # otherwise, the last opened bracket must match
            last_opened_bracked = stack.pop()
            if ch != OPEN_CLOSE_MAPPER[last_opened_bracked]:
                return ch
    return None


def autocomplete_line(line: str) -> List[str]:
    stack = []
    for ch in line:
        # if open bracket, append to the end of the stack
        if ch in OPEN_CLOSE_MAPPER:
            stack.append(ch)
        else:
            # otherwise, the last opened bracket must match
            last_opened_bracked = stack.pop()
            assert ch == OPEN_CLOSE_MAPPER[last_opened_bracked] 
    assert len(stack) > 0
    # return the corresponding closing bracket 
    return [OPEN_CLOSE_MAPPER[ch] for ch in reversed(stack)]



def compute_syntax_score(line: str) -> int:
    if corruped_chunk := get_first_corrupted_bracket(line):
        return SYNTAX_POINT[corruped_chunk]
    return 0


def compute_autocomplete_score(line: str) -> int:
    autocompleted_line = autocomplete_line(line)
    return functools.reduce(lambda score, ch: score * 5 + AUTOCOMPLETE_POINT[ch],
                            autocompleted_line, 0)


def compute_total_syntax_error(lines: List[str]) -> int:
    return sum(compute_syntax_score(line) for line in lines)


def compute_middle_autocomplete_score(lines: List[str]) -> int:
    scores = sorted([compute_autocomplete_score(line) 
                     for line in lines
                     if not get_first_corrupted_bracket(line)])
    # check for odd number of lines
    assert len(scores) % 2 == 1
    return scores[len(scores)//2]




assert get_first_corrupted_bracket('{()()()>') == '>'
assert compute_syntax_score('{()()()>') == 25137
assert compute_syntax_score('()()(') == 0
assert autocomplete_line('[({(<(())[]>[[{[]{<()<>>') == list('}}]])})]')
assert compute_autocomplete_score('[({(<(())[]>[[{[]{<()<>>') == 288957


LINES = RAW.splitlines()
test_case_sol1 = compute_total_syntax_error(LINES)
assert test_case_sol1 == 26397

test_case_sol2 = compute_middle_autocomplete_score(LINES)
assert test_case_sol2 == 288957

if __name__ == '__main__':
    with open('data/input.txt') as f:
        contest_raw = f.read()

    contest_lines = contest_raw.splitlines()
    contest_sol_part1 = compute_total_syntax_error(contest_lines)
    print(contest_sol_part1)
    assert contest_sol_part1 == 390993

    contest_sol_part2 = compute_middle_autocomplete_score(contest_lines)
    print(contest_sol_part2)

    assert contest_sol_part2 == 2391385187


