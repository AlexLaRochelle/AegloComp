from commande import Commande
from drone import Drone
from entrepot import Entrepot
from grid import Grid


class SolutionMaker:
    def __init__(self, grid: Grid, products_weights: [int], entrepots: [Entrepot], commandes: [Commande], drones: [Drone], turn_amount: int):
        self.grid = grid
        self.products_weights = products_weights
        self.entrepots = entrepots
        self.commandes = commandes
        self.drones = drones
        self.turn_amount = turn_amount

        self.products_dict = {
            # id de produit
            '0': {
                'weight': 10,
                'destinations': {
                    # nbr de ce produit nécessaire à la position
                    '(1,1)': 1,
                    '(3,3)': 1
                },
                'origins': {
                    '(0,0)': 5
                }
            },
            '2': {
                'weight': 15,
                'destinations': {
                    # nbr de ce produit nécessaire à la position
                    '(1,1)': 1,
                    '(5,6)': 1
                },
                'origins': {
                    '(5,5)': 2
                }
            }
        }

    def makeSolution(self):

        for turn in range(self.turn_amount):
            for drone in self.drones:
                if not drone.available:
                    continue


                entrepot_id_to_go_to = -1

                while entrepot_id_to_go_to == -1:
                    entrepot_id, distance = self.grid.findClosestEntrepot(self.entrepots, drone.pos)

                    for product in self.entrepots[entrepot_id].products:
                        if self.products_dict[product] and len(self.products_dict[product]['destinations'].keys()) > 0:
                            entrepot_id_to_go_to = entrepot_id




        return "EZ WIN"
