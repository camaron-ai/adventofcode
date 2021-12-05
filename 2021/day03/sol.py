from typing import List

RAW = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""

def is_one_most_common_bit(bits: List[str]) -> bool:
    return sum(map(lambda b: b == '1', bits)) >= len(bits) // 2


def compute_sub_power_consumption(bit_seq: List[str]) -> int:
    gamma, eps = 0, 0
    for bits in zip(*bit_seq):
        most_common_is_1bit = is_one_most_common_bit(bits)
        gamma = 2 * gamma + most_common_is_1bit
        eps = 2 * eps + (not most_common_is_1bit)
    return gamma * eps


def compute_life_support_rating(bit_seq: List[str]) -> int:
    def _compute_life_support(bit_seq: List[str],
                              bit_pos: int,
                              most_common: int) -> int:
        if len(bit_seq) == 1:
            return int(bit_seq[0], 2)
        assert bit_pos < len(bit_seq[0])
        ones, zeros = [], []

        for bit in bit_seq:
            if bit[bit_pos] == '1':
                ones.append(bit)
            else:
                zeros.append(bit)

        most_common_is_1bit = len(ones) >= len(zeros)
        filtered_bit_seq = ((ones if most_common_is_1bit else zeros)
                             if most_common else
                             (zeros if most_common_is_1bit else ones))
        return _compute_life_support(filtered_bit_seq, bit_pos+1, most_common)
    
    return _compute_life_support(bit_seq, 0, True) * _compute_life_support(bit_seq, 0, False)
        


if __name__ == '__main__':
    INPUT = RAW.strip().splitlines()
    sol1_base_case = compute_sub_power_consumption(INPUT)
    print('test case sol part 1')
    print(sol1_base_case)
    assert sol1_base_case == 198

    sol2_base_case = compute_life_support_rating(INPUT)
    print('test case sol part 2')
    print(sol2_base_case)

    assert sol2_base_case == 230

    with open('data/input.txt') as f:
        raw = f.read()
    TEST_INPUT = raw.strip().splitlines()

    sol1_test_output = compute_sub_power_consumption(TEST_INPUT)
    print('contest sol part 1')
    print(sol1_test_output)
    print('contest sol part 2')
    sol2_test_output = compute_life_support_rating(TEST_INPUT)
    print(sol2_test_output)