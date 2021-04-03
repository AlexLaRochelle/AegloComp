from position import Position


class Drone:
    def __init__(self, max_weight, pos: Position):
        self.pos = pos
        self.max_weight = max_weight
