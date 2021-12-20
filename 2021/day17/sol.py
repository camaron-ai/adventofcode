from typing import NamedTuple, Tuple, List


Range = Tuple[int, int]
Velocity = Tuple[int, int]


class Area(NamedTuple):
    low_x: int
    high_x: int
    low_y: int
    high_y: int

    def isin(self, x: int, y: int):
        return (self.low_x <= x <= self.high_x and
                self.low_y <= y <= self.high_y)

    @staticmethod
    def parse(raw_string: str) -> 'Area':
        raw_string = raw_string[13: ]
        x_range_str, y_range_str = raw_string.split(', ')

        x_range = tuple(map(int, x_range_str[2:].split('..')))
        y_range = tuple(map(int, y_range_str[2:].split('..')))
        return Area(low_x=min(x_range), high_x=max(x_range),
                    low_y=min(y_range), high_y=max(y_range))



def sign(x: int) -> int:
    return 1 if x > 0 else -1


def probe_will_reach_target(velocity: Velocity, area: Area) -> bool:
    """Iterate from a pos (0, 0) with velocity (xv, yv) up to getting at the area.
    
    Returns
        bool: Where the probe reached the target
    """

    x_pos = y_pos = 0
    vx, vy = velocity
    max_y_pos = y_pos

    while all([x_pos <= area.high_x, # has no reach the x limit yet
              not (vx == 0 and x_pos < area.low_x), # the vx is 0 and has not reach the x lower limit 
              not (x_pos > area.low_x and y_pos < area.low_y) # reach the x and y lower limit
              ]):
        x_pos += vx
        y_pos += vy
        if vx > 0:
            vx -= sign(vx)
        vy -= 1

        max_y_pos = max(y_pos, max_y_pos)

        if area.isin(x_pos, y_pos):
            return True
    return False


def find_all_velocities(area: Area) -> List[Velocity]:
    velocities = []
    for vx in range(1, area.high_x * 2):
        for vy in range(area.low_y, area.high_x):
            on_target = probe_will_reach_target((vx, vy), area)
            if on_target:
                velocities.append((vx, vy))
    return velocities


def find_max_y_pos(velocities: List[Velocity]):
    return max(y * (y + 1) // 2 for _, y in velocities)


AREA = Area.parse("target area: x=20..30, y=-10..-5")
VELOCITIES = find_all_velocities(AREA)

MAX_Y_POS = find_max_y_pos(VELOCITIES)
assert MAX_Y_POS == 45
assert len(VELOCITIES) == 112


if __name__ == '__main__':

    contest_area = Area.parse("target area: x=156..202, y=-110..-69")
    velocities = find_all_velocities(contest_area)

    max_y_pos = find_max_y_pos(velocities)
    print('contest sol part 1')
    print(max_y_pos)
    print('contest sol part 2')    
    print(len(velocities))