from typing import List


RAW = """199
200
208
210
200
207
240
269
260
263"""

def count_increasing(input: List[int], gap: int = 1) -> int:
    count = 0
    for i in range(len(input)-gap):
        if input[i + gap] > input[i]:
            count += 1
    return count

if __name__ == '__main__':
    INPUT = [int(x) for x in RAW.strip().split('\n')]
    print('test case sol part 1')
    print(count_increasing(INPUT))
    print('test case sol part 2')
    print(count_increasing(INPUT, gap=3))
    with open('data/input.txt') as f:
        raw = f.read()
    CONTEST_INPUT = [int(x) for x in raw.strip().split('\n')]
    print('contest solution part 1')
    print(count_increasing(CONTEST_INPUT))
    print('contest solution part 2')
    print(count_increasing(CONTEST_INPUT, gap=3))