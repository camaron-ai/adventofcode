from typing import List, NamedTuple
import itertools
from collections import Counter

RAW = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""


DIGIT_MAPPER = {'abcefg': 0,
                'cf': 1, 
                'acdeg': 2,
                'acdfg': 3,
                'bcdf': 4,
                'abdfg': 5,
                'abdefg': 6,
                'acf': 7,
                'abcdefg': 8,
                'abcdfg': 9
                }


class Display(NamedTuple):
    output_digits: List[str]
    signal_pattern: List[str]

    @staticmethod
    def parse(raw: str) -> 'Display':
        signal_pattern_str, output_digits_str = raw.split(' | ')

        signal_pattern = signal_pattern_str.strip().split()
        output_digits = output_digits_str.strip().split()

        return Display(output_digits, signal_pattern)


def count_digits_1478(displays: List[Display]) -> int:
    return sum(len(digit) in [2, 3, 4, 7]
               for display in displays
               for digit in display.output_digits)


def decode_7sg_digit(display: Display) -> int:
    # sort the digits by their lenght
    display.signal_pattern.sort(key=lambda x: len(x))
    counts = Counter(itertools.chain(*display.signal_pattern))
    mapping = {}
    wires = 'abcdefg'
    # find e b f by their counts
    for wire in wires:
        if counts[wire] == 4:
            mapping[wire] = 'e'
        elif counts[wire] == 6:
            mapping[wire] = 'b'
        elif counts[wire] == 9:
            mapping[wire] = 'f'
    
    # one is cf, only missing c
    one = display.signal_pattern[0]
    c_segment = next(c for c in one if c not in mapping)
    mapping[c_segment] = 'c'
    # found b, c, e, f

    # seven is a c f, only missing a
    seven = display.signal_pattern[1]
    a_segment = next(c for c in seven if c not in mapping)
    mapping[a_segment] = 'a'
    # found a, b, c, e, f

    # four is b d c f, only missing d
    four = display.signal_pattern[2]
    d_segment = next(c for c in four if c not in mapping)
    mapping[d_segment] = 'd'
    # found a, b, c, d, e, f
    
    # now only missing g
    g_segment = next(c for c in wires if c not in mapping)
    mapping[g_segment] = 'g'

    # decode the output values
    output = 0
    for digit in display.output_digits:
        decoded_digit = ''.join(sorted(mapping[c] for c in digit))
        digit = DIGIT_MAPPER[decoded_digit]
        output = output * 10 + int(digit)
    return output


def sum_and_decode_digits(displays: List[Display]) -> int:
    return sum(map(decode_7sg_digit, displays))


DISPLAYS = list(map(Display.parse, RAW.splitlines()))
test_case_sol1 = count_digits_1478(DISPLAYS)

assert test_case_sol1 == 26

assert decode_7sg_digit(DISPLAYS[0]) == 8394
test_case_sol2 = sum_and_decode_digits(DISPLAYS)
assert test_case_sol2 == 61229



if __name__ == '__main__':
    with open('data/input.txt') as f:
        contest_raw = f.read()

    contest_displays = list(map(Display.parse, contest_raw.splitlines()))
    contest_sol_part1 = count_digits_1478(contest_displays)
    print('contest sol part 1')
    print(contest_sol_part1)
    assert contest_sol_part1 == 274

    contest_sol_part2 = sum_and_decode_digits(contest_displays)
    print('contest sol part 2')
    print(contest_sol_part2)
    assert contest_sol_part2 == 1012089

