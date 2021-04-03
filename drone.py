import enum

from position import Position


class DroneState(enum.Enum):
    TRAVELING = 1
    ACTION_PICKING = 2
    ACTION_DROPPING = 3
    NOTHING = 4


class Drone:
    def __init__(self, max_weight, pos: Position):
        self.pos = pos
        self.max_weight = max_weight
        self.available = True
        self.state = DroneState.NOTHING
