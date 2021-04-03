from position import Position


class Entrepot:
    def __init__(self, pos: Position, products: [int], entrepot_id: int):
        self.pos = pos
        self.products = products
        self.entrepot_id = entrepot_id
        self.utile = True

    def __str__(self):
        return 'Pos: ' + str(self.pos) + '\nProducts: ' + str(self.products) + '\n'

    def __repr__(self):
        return self.__str__()
