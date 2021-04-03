from commande import Commande
from drone import Drone
from entrepot import Entrepot
from grid import Grid


class SolutionMaker:
    def __init__(self, grid: Grid, products_weights: [int], entrepots: [Entrepot], commandes: [Commande], drones: [Drone]):
        self.grid = grid
        self.products_weights = products_weights
        self.entrepots = entrepots
        self.commandes = commandes
        self.drones = drones

    def makeSolution(self):

        return "EZ WIN"
