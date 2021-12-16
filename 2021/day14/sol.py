from typing import Dict, Counter

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


def polymeter_to_pair_count(polymer: str) -> Dict[str, int]:
    return Counter(polymer[i: i+2] for i in range(len(polymer) - 1))


class Polymerization:
    def __init__(self, polymer: str, insection_pairs: Dict[str, str]):
        self.pair_count = polymeter_to_pair_count(polymer)
        self.insection_pairs = insection_pairs
        self.element_count = Counter(polymer)

    def step(self) -> None:
        new_pairs = Counter()
        for pair, count in self.pair_count.items():
            if pair in self.insection_pairs:
                element = self.insection_pairs[pair]
                new_pairs[pair[0] + element] += count
                new_pairs[element + pair[1]] += count
                self.element_count[element] += count
        self.pair_count = new_pairs
    
    def compute_most_least_common_difference(self) -> int:
        sorted_counts = self.element_count.most_common()
        most_common_count = sorted_counts[0][1]
        least_common_count = sorted_counts[-1][1]
        return most_common_count - least_common_count


    @staticmethod
    def parse(raw_string: str) -> 'Polymerization':
        polymer_template, raw_insection_pairs = raw_string.strip().split('\n\n')
        insection_pairs = dict(row.split(' -> ') for row in raw_insection_pairs.splitlines())
        return Polymerization(polymer_template, insection_pairs)



EXPECTED_SOL1 = ['NCNBCHB', 'NBCCNBBBCBHCB',
                 'NBBBCNCCNBBNBNBBCHBHHBCHB',
                 'NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB']

POLYMETER = Polymerization.parse(RAW)
for i in range(len(EXPECTED_SOL1)):
    POLYMETER.step()
    expected_pair = polymeter_to_pair_count(EXPECTED_SOL1[i])
    expected_count = Counter(EXPECTED_SOL1[i])
    assert expected_count == POLYMETER.element_count
    assert expected_pair == POLYMETER.pair_count

for _ in range(6):
    POLYMETER.step()
test_case_sol1 = POLYMETER.compute_most_least_common_difference()
assert test_case_sol1 == 1588

for _ in range(30):
    POLYMETER.step()
test_case_sol2 = POLYMETER.compute_most_least_common_difference()
assert test_case_sol2 == 2188189693529
    


if __name__ == '__main__':
    with open('data/input.txt') as f:
        contest_raw = f.read()
    contest_polymeter = POLYMETER.parse(contest_raw)
    for _ in range(10):
        contest_polymeter.step()
    contest_sol_part1 = contest_polymeter.compute_most_least_common_difference()
    print(contest_sol_part1)

    for _ in range(30):
        contest_polymeter.step()
    contest_sol_part2 = contest_polymeter.compute_most_least_common_difference()
    print(contest_sol_part2)