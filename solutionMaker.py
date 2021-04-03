from pprint import pprint

from commande import Commande
from drone import Drone
from entrepot import Entrepot
from grid import Grid

DESTINATIONS_KEY = 'destinations'
WEIGHT_KEY = 'weight'
ORIGINS_KEY = 'origins'

class SolutionMaker:
    def __init__(self, grid: Grid, products_weights: [int], entrepots: [Entrepot], commandes: [Commande], drones: [Drone], turn_amount: int):
        self.grid = grid
        self.products_weights = products_weights
        self.entrepots = entrepots
        self.commandes = commandes
        self.drones = drones
        self.turn_amount = turn_amount
        self.products_dict = self.createProductsDict()
        self.solution = {}
        for drone in drones:
            self.solution[drone.id] = []

    def createProductsDict(self):
        productsDict = {}
        for commande in self.commandes:
            for productId in commande.products_ids:
                if productId not in productsDict:
                    productsDict[productId] = {
                        WEIGHT_KEY: self.products_weights[productId],
                        DESTINATIONS_KEY: {
                            str(commande.pos): 1
                        },
                        ORIGINS_KEY: {}
                    }
                    for entrepot in self.entrepots:
                        if entrepot.products[productId] > 0:
                            productsDict[productId][ORIGINS_KEY][str(entrepot.pos)] = entrepot.products[productId]
                else:
                    if commande.pos not in productsDict[productId][DESTINATIONS_KEY]:
                        productsDict[productId][DESTINATIONS_KEY][str(commande.pos)] = 1
                    else:
                        productsDict[productId][DESTINATIONS_KEY][str(commande.pos)] += 1
        pprint(productsDict)
        return productsDict

    def issueOrderLoad(self, drone_id, entrepot, type_produit, quantite):
        self.solution[id].append(drone_id + ' ' + 'L' + ' ' + entrepot + ' ' + type_produit + ' ' + quantite)

    def issueOrderUnload(self, drone_id, entrepot, type_produit, quantite):
        self.solution[id].append(drone_id + ' ' + 'U' + ' ' + entrepot + ' ' + type_produit + ' ' + quantite)

    def issueOrderDeliver(self, drone_id, entrepot, type_produit, quantite):
        self.solution[id].append(drone_id + ' ' + 'D' + ' ' + entrepot + ' ' + type_produit + ' ' + quantite)

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
