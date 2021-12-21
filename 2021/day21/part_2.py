from typing import Tuple, Optional, Dict
import itertools
from collections import Counter


Player = Tuple[int, int]
P1P2Key = Tuple[int, int, int, int]
WinCount = Tuple[int, int]
Memo = Dict[P1P2Key, WinCount]
possible_dice_outcomes = Counter(map(sum, list(itertools.product((1, 2, 3), repeat=3))))


def parse_player(raw_string: str) -> Player:
    _, str_pos = raw_string.split(':')
    return int(str_pos), 0

def parse(raw_string: str) -> Tuple[Player, Player]:
    players = [parse_player(p) for p in raw_string.splitlines()]
    return players

def move_player(p: Player, step: int) -> Player:
    new_pos = p[0] + step
    if new_pos % 10 == 0:
        new_pos = 10
    elif new_pos > 10:
        new_pos = new_pos % 10
    score = p[1] + new_pos
    return (new_pos, score)


assert move_player((10, 0), 10) == (10, 10)
assert move_player((4, 0), 6) == (10, 10)
assert move_player((10, 10), 24) == (4, 14)


def multiverse_game(p1: Player, p2: Player,
                    winning_score: int,
                    memo: Optional[Memo] = None) -> WinCount:
    """
    return the times each player won using the quantum dice
    return:
        WinCount: Tuple[int, int]
    """
    if memo is None:
        memo = {}
    try:
        # try to access precompute result
        return memo[(p1[0], p1[1], p2[0], p2[1])]
    except KeyError:
        count = [0, 0]
        # for each possible dice combination
        for rolls_p1, roll_count_p1 in possible_dice_outcomes.items():
            # move the player 1
            parallel_p1 = move_player(p1, rolls_p1)
            # if player one wins, sum roll_count_p1 to his count
            # player two do not have to roll the dice because game is over
            if parallel_p1[1] >= winning_score:
                count[0] += roll_count_p1
            else:
                # if not, roll the dice for player 2
                for rolls_p2, roll_count_p2 in possible_dice_outcomes.items():
                    # if player 2 wins, sum roll_count_p2 to his count
                    parallel_p2 = move_player(p2, rolls_p2)
                    if parallel_p2[1] >= winning_score:
                        count[1] += roll_count_p1 * roll_count_p2
                    else:
                        # otherwise, any player has won,
                        # so recursivily add the count of the parrelel game
                        # there is a total of roll_count_p1 * roll_count_p2 to get to this combination
                        # so, the number of wins of each player will be multiplied by roll_count_p1 * roll_count_p2
                        total_rolls = roll_count_p1 * roll_count_p2
                        parralel_count = multiverse_game(parallel_p1, parallel_p2,
                                                         winning_score, memo)
                        count[0] += total_rolls * parralel_count[0]
                        count[1] += total_rolls * parralel_count[1]
        # add the result to the current game
        memo[(p1[0], p1[1], p2[0], p2[1])] = count
        return count


RAW = """Player 1 starting position: 4
Player 2 starting position: 8"""

P1, P2 = parse(RAW)
WINNING_SCORE = 21
WIN_COUNTS = multiverse_game(P1, P2, winning_score=WINNING_SCORE)
assert WIN_COUNTS[0] == 444356092776315, WIN_COUNTS[0]
assert WIN_COUNTS[1] == 341960390180808, WIN_COUNTS[1]
assert max(WIN_COUNTS) == 444356092776315


if __name__ == '__main__':
    contest_raw = """Player 1 starting position: 10
# Player 2 starting position: 1"""
    contest_p1, contest_p2 = parse(contest_raw)
    contest_win_counts = multiverse_game(contest_p1, contest_p2, winning_score=WINNING_SCORE)
    print('contest sol part 2')
    print(max(contest_win_counts))