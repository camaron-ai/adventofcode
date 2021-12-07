from typing import List


RAW = """3,4,3,1,2"""


def count_lanternfish(fish_timers: List[int],
                      ndays: int = 80) -> int:

    timers =  [0 for _ in range(9)]

    for fish_timer in fish_timers:
        timers[fish_timer] += 1

    for _ in range(ndays):
        n = timers.pop(0)
        timers[6] += n
        timers.append(n)

    return sum(timers)


if __name__ == '__main__':

    INPUT = list(map(int, RAW.split(',')))

    test_case_sol1 = count_lanternfish(INPUT)
    print('test case sol part 1')
    print(test_case_sol1)
    assert test_case_sol1 == 5934

    test_case_sol2 = count_lanternfish(INPUT, 256)
    print('test case sol part 2')
    print(test_case_sol2)
    assert test_case_sol2 == 26984457539


    with open('data/input.txt') as f:
        contest_raw = f.read()
    contest_input = list(map(int, contest_raw.split(',')))

    contest_sol1 = count_lanternfish(contest_input)
    print('contest sol part 1')
    print(contest_sol1)

    contest_sol2 = count_lanternfish(contest_input, 256)
    print('contest sol part 2')
    print(contest_sol2)
