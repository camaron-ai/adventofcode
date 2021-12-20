"""
Snailfist numbers are pairs as
[1,2]
[[1,2],3]

each item could be a regular number of another pair

to sum 2 numbers

[1, 2] + [[3, 4], 5] = [[1, 2], [[3, 4], 5]]

all numbers must always be reduced

to reduced a number:
    1. If any pair is nested inside four pairs, the leftmost such pair explodes.
    2. If any regular number is 10 or greater, the leftmost such regular number splits.

apply until no action above can be done.
the opreation must be carried on in order, first explodes then splits.


to explode a pair

9 sum to left regular number (None), 8 + 1, pair [9, 8] goes to 0
[[[[[9,8],1],2],3],4] becomes [[[[0,9],2],3],4]


"""

from typing import Iterable, List, Tuple, Union
from dataclasses import dataclass


Entry = Union[int, Tuple[int, int]]
RawPairType = Tuple[Entry, Entry]

@dataclass
class Pair:
    left: Union['Pair', int]
    right: Union['Pair', int]

    def is_left_regular(self) -> bool:
        return isinstance(self.left, int)
    
    def is_right_regular(self) -> bool:
        return isinstance(self.right, int)

    def both_regular(self) -> bool:
        return self.is_left_regular() and self.is_right_regular()
    
    @staticmethod
    def from_list(pair: RawPairType) -> 'Pair':
        left = pair[0] if isinstance(pair[0], int) else Pair.from_list(pair[0])
        right = pair[1] if isinstance(pair[1], int) else Pair.from_list(pair[1])
        return Pair(left, right)



# assert join_numbers([1,2], [[3,4],5]) == [[1,2],[[3,4],5]]
# assert join_numbers([[[[4,3],4],4],[7,[[8,4],9]]], [1,1]) == [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]

PAIR = Pair.from_list([[6,[5,[4,[3,2]]]],1]) 


def iterate_pair(pair: Pair) -> Iterable:
    if pair.both_regular():
        yield pair
        return 
    
    if pair.is_left_regular():
        yield pair.left
    
    else:
        yield from iterate_pair(pair.left)

    if pair.is_right_regular():
        yield pair.right
    
    else:
        yield from iterate_pair(pair.right)


print(PAIR)


x = [x for x in iterate_pair(PAIR)]
print(x)