import enum

from position import Position


class DroneState(enum.Enum):
    TRAVELING_TO_DROP = 1
    TRAVELING_TO_ENTREPOT = 2
    ACTION_PICKING = 3
    ACTION_DROPPING = 4
    NOTHING = 5


class Drone:
    def __init__(self, max_weight, pos: Position):
        self.pos = pos
        self.max_weight = max_weight
        self.current_weight = 0
        self.state = DroneState.TRAVELING_TO_ENTREPOT
        self.entrepot_id_going = 0
        self.destinations = []
        self.turns_to_destination = 0
        self.carrying = []
