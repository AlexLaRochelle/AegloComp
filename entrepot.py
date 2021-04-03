from position import Position


class Entrepot:
    def __init__(self, pos: Position, products):
        self.pos = pos
        self.products = products

    def __str__(self):
        return 'Pos: ' + str(self.pos) + '\nProducts: ' + str(self.products) + '\n'

    def __repr__(self):
        return self.__str__()
