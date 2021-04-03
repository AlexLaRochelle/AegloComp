from position import Position


class Commande:
    def __init__(self, pos: Position, products_ids):
        self.pos = pos
        self.products_ids = {}

        for product_id in products_ids:
            if product_id not in self.products_ids:
                self.products_ids[product_id] = 1
            else:
                self.products_ids[product_id] += 1

    def __str__(self):
        return 'Pos: ' + str(self.pos) + ', Products: ' + str(self.products_ids) + '\n'

    def __repr__(self):
        return self.__str__()
