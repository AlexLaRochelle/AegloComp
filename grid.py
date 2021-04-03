import math
from math import sqrt

from entrepot import Entrepot
from position import Position


class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def findClosestEntrepot(self, entrepots: [Entrepot], pos: Position):
        best_distance = 9999999
        best_entrepot_id = -1

        for entrepot in entrepots:
            distance = pos.distanceTo(entrepot.pos)

            if distance < best_distance:
                best_distance = distance
                best_entrepot_id = entrepot.entrepot_id

        if best_entrepot_id == -1 or best_distance == 9999999:
            print("SOMETHING VERY BAD HAPPENED")

        return best_entrepot_id, best_distance

    def findClosest(self, posToCheck, pos2: Position):
        best_distance = 9999999
        best_position = Position(0, 0)

        for pos in posToCheck:
            distance = pos2.distanceTo(pos)

            if distance < best_distance:
                best_distance = distance
                best_position = pos

        if best_distance == 9999999:
            return None, None

        return best_position, math.ceil(best_distance)
