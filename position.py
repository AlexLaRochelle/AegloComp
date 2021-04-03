from math import sqrt


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distanceTo(self, otherPos):
        return \
            sqrt(pow(abs(otherPos.pos.x - self.x), 2)) + \
            sqrt(pow(abs(otherPos.pos.y - self.y), 2))

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
