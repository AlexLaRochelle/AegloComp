from commande import Commande
from entrepot import Entrepot
from grid import Grid


class SolutionMaker:
    def __init__(self, grid: Grid, products_weights: [int], entrepots: [Entrepot], commandes: [Commande]):
        self.grid = grid
        self.products_weights = products_weights
        self.entrepots = entrepots
        self.commandes = commandes

    def makeSolution(self):
        return "EZ WIN"
