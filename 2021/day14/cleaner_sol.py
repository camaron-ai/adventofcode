from typing import Dict, Tuple
from collections import Counter


RAW = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


Rules = Dict[str, str]

def parse_input(raw_string: str) -> Tuple[str, Rules]:
    polymer_template, raw_rules = raw_string.strip().split('\n\n')
    rules = dict(row.split(' -> ') for row in raw_rules.splitlines())
    return polymer_template, rules


def polymeter_to_pair_count(polymer: str) -> Dict[str, int]:
    return Counter(polymer[i: i+2] for i in range(len(polymer) - 1))


def polymerization(polymer: str, rules: Rules, steps: int):
    element_count = Counter(polymer)
    pair_count = polymeter_to_pair_count(polymer)

    for _ in range(steps):
        new_pairs = Counter()
        for pair, count in pair_count.items():
            if pair in rules:
                element = rules[pair]
                new_pairs[pair[0] + element] += count
                new_pairs[element + pair[1]] += count
                element_count[element] += count
        pair_count = new_pairs

    sorted_counts = element_count.most_common()
    most_common_count = sorted_counts[0][1]
    least_common_count = sorted_counts[-1][1]
    return most_common_count - least_common_count


POLYMETER, RULES = parse_input(RAW)
test_case_sol1 = polymerization(POLYMETER, RULES, 10)
assert test_case_sol1 == 1588

test_case_sol2 = polymerization(POLYMETER, RULES, 40)
assert test_case_sol2 == 2188189693529
    


if __name__ == '__main__':
    with open('data/input.txt') as f:
        contest_raw = f.read()
    contest_polymeter, contest_rules = parse_input(contest_raw)
    contest_sol_part1 = polymerization(contest_polymeter, contest_rules, 10)
    print(contest_sol_part1)

    contest_sol_part2 =polymerization(contest_polymeter, contest_rules, 40)
    print(contest_sol_part2)