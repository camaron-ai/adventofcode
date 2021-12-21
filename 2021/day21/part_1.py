from dataclasses import dataclass
from typing import Optional, List


@dataclass
class DeterministicDice:
    sides: Optional[int] = 100
    i: Optional[int] = 1

    def roll(self) -> int:
        out = self.i
        self.i += 1
        if self.i > self.sides:
            self.i = 1
        return out
    
    def roll_n_times(self, n: int) -> List[int]:
        return [self.roll() for _ in range(n)]

@dataclass
class Player:
    pos: int
    score: Optional[int] = 0

    def move(self, steps: List[int]) -> None:
        new_pos = (self.pos + sum(steps))
        if new_pos % 10 == 0:
            new_pos = 10
        elif new_pos > 10:
            new_pos = new_pos % 10
        self.pos = new_pos
        self.score += self.pos
    
    @staticmethod
    def parse(raw_string: str) -> 'Player':
        _, str_pos = raw_string.split(':')
        return Player(int(str_pos))


P = Player(4)
P.move([1, 2, 3])
assert P.score == 10
assert P.pos == 10

P.move([7, 8, 9])
assert P.score == 14
assert P.pos == 4

P = Player(10)
P.move([5, 4, 1])
assert P.score == 10
assert P.pos == 10

        

class Game:
    def __init__(self, players: List[Player],
                dice_side: int,
                winning_score: int = 1000) -> None:
        self.players = players
        self.dice = DeterministicDice(dice_side)
        self.winning_score = winning_score
    
    def play(self) -> int:
        """play until any of the players reach the winning score
        return the number of rolls * the loser score """
        found_winner = False
        n_rolls = 0
        while True:
            for p in self.players:
                moves = self.dice.roll_n_times(3)
                n_rolls += 3
                p.move(moves)
                if p.score >= self.winning_score:
                    found_winner = True
                    break
            if found_winner:
                break
        return min(n_rolls * p.score for p in self.players)

    @staticmethod
    def parse(raw_string: str, dice_side: int, winning_score: int) -> 'Game':
        players = [Player.parse(p) for p in raw_string.splitlines()]
        return Game(players, dice_side, winning_score)


RAW = """Player 1 starting position: 4
Player 2 starting position: 8"""


WIN_SCORE = 1000
DICE_SIZE = 100
GAME = Game.parse(RAW, DICE_SIZE, WIN_SCORE)

test_case_sol1 = GAME.play()
assert test_case_sol1 == 739785

if __name__ == '__main__':
    contest_raw = """Player 1 starting position: 10
Player 2 starting position: 1"""
    contest_game = Game.parse(contest_raw, DICE_SIZE, WIN_SCORE)

    contest_sol_part1 = contest_game.play()
    print('contest sol part 1')
    print(contest_sol_part1)