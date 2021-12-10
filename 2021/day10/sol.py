from typing import List, Tuple
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


CLOSE_OPEN_MAPPER = {')': '(', ']': '[', '}': '{', '>': '<'}
OPEN_CLOSE_MAPPER = {op: close for close, op in CLOSE_OPEN_MAPPER.items()}


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


def get_line_status(line: str) -> Tuple[int, str]:
    stack = []
    for ch in line:
        if ch in CLOSE_OPEN_MAPPER:
            last_opened_bracked = stack.pop()
            if last_opened_bracked != CLOSE_OPEN_MAPPER[ch]:
                return (1, ch)
        else:
            stack.append(ch)
    if len(stack) > 0:
        return (2, ''.join(OPEN_CLOSE_MAPPER[ch] for ch in reversed(stack)))
    return (0, '')



def compute_syntax_error(line: str) -> int:
    status, corruped_chunk = get_line_status(line)
    if status == 1:
        return SYNTAX_POINT[corruped_chunk]
    return 0


def compute_autocomplete_score(autocompleted_line: str) -> int:
    return functools.reduce(lambda score, ch: score * 5 + AUTOCOMPLETE_POINT[ch],
                            autocompleted_line, 0)


def compute_total_syntax_error(lines: List[str]) -> int:
    return sum(compute_syntax_error(line) for line in lines)


def compute_middle_autocomplete_score(lines: List[str]) -> int:
    incomplete_lines = []
    for line in lines:
        status, autocompleted_line = get_line_status(line)
        if status == 2:
            incomplete_lines.append(autocompleted_line)
    scores = sorted([compute_autocomplete_score(autocompleted_line)
                     for autocompleted_line in incomplete_lines])
    return scores[len(scores)//2]




assert get_line_status('{()()()>') == (1, '>')
assert compute_syntax_error('{()()()>') == 25137
assert compute_syntax_error('()()(') == 0
assert get_line_status('[({(<(())[]>[[{[]{<()<>>') == (2, '}}]])})]')
assert compute_autocomplete_score('])}>') == 294


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


    contest_sol_part2 = compute_middle_autocomplete_score(contest_lines)
    print(contest_sol_part2)



