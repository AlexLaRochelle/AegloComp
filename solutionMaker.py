from commande import Commande
from drone import Drone, DroneState
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

        # self.products_dict = {
        #     # id de produit
        #     '0': {
        #         'weight': 10,
        #         'destinations': {
        #             # nbr de ce produit nécessaire à la position
        #             '(1,1)': 1,
        #             '(3,3)': 1
        #         },
        #         'origins': {
        #             '(0,0)': 5
        #         }
        #     },
        #     '2': {
        #         'weight': 15,
        #         'destinations': {
        #             # nbr de ce produit nécessaire à la position
        #             '(1,1)': 1,
        #             '(5,6)': 1
        #         },
        #         'origins': {
        #             '(5,5)': 2
        #         }
        #     }
        # }


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
        return productsDict

    def issueOrderLoad(self, drone_id, entrepot, type_produit, quantite):
        orderString = str(drone_id) + ' ' + 'L' + ' ' + str(entrepot) + ' ' + str(type_produit) + ' ' + str(quantite)
        self.solution[drone_id].append(orderString)
        print(orderString)

    def issueOrderUnload(self, drone_id, entrepot, type_produit, quantite):
        self.solution[drone_id].append(str(drone_id) + ' ' + 'U' + ' ' + str(entrepot) + ' ' + str(type_produit) + ' ' + str(quantite))

    def issueOrderDeliver(self, drone_id, commande_id, type_produit, quantite):
        orderString = str(drone_id) + ' ' + 'D' + ' ' + str(commande_id) + ' ' + str(type_produit) + ' ' + str(quantite)
        self.solution[drone_id].append(str(drone_id) + ' ' + 'D' + ' ' + str(commande_id) + ' ' + str(type_produit) + ' ' + str(quantite))
        print(orderString)

    def makeActualSolution(self):
        slnFile = open('sln', 'w')
        superMegaSlnString = ""

        orderCount = 0
        for drone in self.solution:
            for order in self.solution[drone]:
                superMegaSlnString += order + "\n"
                orderCount += 1

        actualString = str(orderCount) + '\n' + superMegaSlnString
        slnFile.write(actualString)

        slnFile.close()

    def makeSolution(self):
        for turn in range(self.turn_amount):
            for drone in self.drones:
                if drone.state == DroneState.TRAVELING_TO_ENTREPOT:
                    if drone.turns_to_destination == 0:
                        drone.pos = self.entrepots[drone.entrepot_id_going].pos
                        drone.state = DroneState.ACTION_PICKING
                        for product_id, product_amount in enumerate(self.entrepots[drone.entrepot_id_going].products):
                            if product_amount == 0:
                                continue

                            if product_id in self.products_dict and len(
                                    self.products_dict[product_id]['destinations'].keys()) > 0:

                                total_products_needed = 0
                                total_carrying_of_this_product = 0
                                product_weight = int(self.products_weights[product_id])

                                for destination in self.products_dict[product_id]['destinations']:
                                    total_products_needed += self.products_dict[product_id]['destinations'][destination]

                                last_best_pos = drone.pos
                                while drone.current_weight + product_weight <= drone.max_weight:

                                    last_best_pos, distance = self.grid.findClosest(
                                        self.products_dict[product_id]['destinations'], last_best_pos)

                                    if last_best_pos is None:
                                        break

                                    best_pos_str = str(last_best_pos)

                                    for product_count in range(
                                            self.products_dict[product_id]['destinations'][best_pos_str]):
                                        if drone.current_weight + product_weight <= drone.max_weight:
                                            if self.products_dict[product_id]['origins'][str(drone.pos)] > 0:
                                                total_carrying_of_this_product += 1
                                                drone.current_weight += product_weight
                                                self.products_dict[product_id]['origins'][str(drone.pos)] -= 1
                                                self.entrepots[drone.entrepot_id_going].products[product_id] -= 1
                                                self.products_dict[product_id]['destinations'][best_pos_str] -= 1
                                                drone.carrying.append(product_id)
                                                drone.destinations.append(last_best_pos)
                                                drone.turns_to_destination = distance
                                            else:
                                                break

                                    if self.products_dict[product_id]['destinations'][best_pos_str] == 0:
                                        self.products_dict[product_id]['destinations'].pop(best_pos_str)
                                    else:
                                        break

                                self.issueOrderLoad(drone.id, drone.entrepot_id_going, product_id, len(drone.carrying))
                                break
                        if len(drone.carrying) == 0:
                            drone.state = DroneState.ACTION_DROPPING
                            print("SOMEONE ROBBED ME FUCK")

                    else:
                        drone.turns_to_destination -= 1

                elif drone.state == DroneState.ACTION_PICKING:
                    carrying_amount_before_code = len(drone.carrying)
                    for product_id, product_amount in enumerate(self.entrepots[drone.entrepot_id_going].products):
                        if product_id not in self.products_dict or len(
                                self.products_dict[product_id]['destinations'].keys()) <= 0:
                            continue

                        product_weight = int(self.products_dict[product_id]['weight'])
                        if drone.current_weight + product_weight > drone.max_weight or product_amount == 0:
                            continue

                        total_products_needed = 0
                        total_carrying_of_this_product = 0

                        for destination in self.products_dict[product_id]['destinations']:
                            total_products_needed += self.products_dict[product_id]['destinations'][destination]

                        last_best_pos = drone.pos
                        while drone.current_weight + product_weight <= drone.max_weight:

                            last_best_pos, distance = self.grid.findClosest(
                                self.products_dict[product_id]['destinations'], last_best_pos)

                            if last_best_pos is None:
                                break

                            best_pos_str = str(last_best_pos)

                            for product_count in range(
                                    self.products_dict[product_id]['destinations'][best_pos_str]):
                                if drone.current_weight + product_weight <= drone.max_weight:
                                    if self.products_dict[product_id]['origins'][str(drone.pos)] > 0:
                                        total_carrying_of_this_product += 1
                                        drone.current_weight += product_weight
                                        self.products_dict[product_id]['origins'][str(drone.pos)] -= 1
                                        self.entrepots[drone.entrepot_id_going].products[product_id] -= 1
                                        self.products_dict[product_id]['destinations'][best_pos_str] -= 1
                                        drone.carrying.append(product_id)
                                        drone.destinations.append(last_best_pos)
                                    else:
                                        break

                            if self.products_dict[product_id]['destinations'][best_pos_str] == 0:
                                self.products_dict[product_id]['destinations'].pop(best_pos_str)
                            else:
                                break

                        items_to_load = 0
                        for i, product_id_test in enumerate(drone.carrying):
                            if product_id_test == product_id:
                                items_to_load += 1

                        self.issueOrderLoad(drone.id, drone.entrepot_id_going, product_id, items_to_load)
                        break

                    if len(drone.carrying) == carrying_amount_before_code:
                        distance = drone.pos.distanceTo(drone.destinations[0])
                        drone.turns_to_destination = distance - 1

                        drone.state = DroneState.TRAVELING_TO_DROP

                elif drone.state == DroneState.TRAVELING_TO_DROP:
                    if drone.turns_to_destination == 0:
                        drone.state = DroneState.ACTION_DROPPING
                        drone.pos = drone.destinations[0]
                        currentItem = drone.carrying[0]
                        items_to_drop = 0
                        for i, product_id_test in enumerate(drone.carrying):
                            if str(drone.destinations[i]) == str(drone.pos) and product_id_test == currentItem:
                                items_to_drop += 1

                        for i in range(items_to_drop):
                            drone.destinations.pop(0)
                            product_id = drone.carrying.pop(0)
                            drone.current_weight -= self.products_weights[product_id]

                        commandeId = -1
                        for i, commande in enumerate(self.commandes):
                            if str(drone.pos) == str(commande.pos):
                                if currentItem in commande.products_ids:
                                    commandeId = i
                                    break

                        if commandeId == -1:
                            print("SOMETHING VERY BAD HAPPENED")
                        self.issueOrderDeliver(drone.id, commandeId, currentItem, items_to_drop)

                    else:
                        drone.turns_to_destination -= 1


                elif drone.state == DroneState.ACTION_DROPPING:
                    if len(drone.destinations) > 0:
                        if drone.pos == drone.destinations[0]:
                            currentItem = drone.carrying[0]
                            items_to_drop = 0
                            for i, product_id_test in enumerate(drone.carrying):
                                if str(drone.destinations[i]) == str(drone.pos) and product_id_test == currentItem:
                                    items_to_drop += 1

                            for i in range(items_to_drop):
                                drone.destinations.pop(0)
                                product_id = drone.carrying.pop(0)
                                drone.current_weight -= self.products_weights[product_id]
                            commandeId = -1
                            for i, commande in enumerate(self.commandes):
                                if str(drone.pos) == str(commande.pos):
                                    if currentItem in commande.products_ids:
                                        commandeId = i
                                        break

                            if commandeId == -1:
                                print("SOMETHING VERY BAD HAPPENED")
                            self.issueOrderDeliver(drone.id, commandeId, currentItem, items_to_drop)
                        else:
                            drone.state = DroneState.TRAVELING_TO_DROP
                            distance = drone.pos.distanceTo(drone.destinations[0])
                            drone.turns_to_destination = distance - 1

                    else:
                        entrepot_id_to_go_to = -1
                        drone.state = DroneState.TRAVELING_TO_ENTREPOT

                        while entrepot_id_to_go_to == -1:
                            entrepot_id, distance = self.grid.findClosestEntrepot(self.entrepots, drone.pos)

                            if entrepot_id is None:
                                print("Setting drone " + str(drone.id) + "to nothing")
                                drone.state = DroneState.NOTHING
                                break

                            for product_id, product_amount in enumerate(self.entrepots[entrepot_id].products):
                                if product_id in self.products_dict and len(
                                        self.products_dict[product_id]['destinations'].keys()) > 0:
                                    entrepot_id_to_go_to = entrepot_id
                                    drone.entrepot_id_going = entrepot_id
                                    drone.turns_to_destination = distance

                            if entrepot_id_to_go_to == -1:
                                self.entrepots[entrepot_id].utile = False

        self.makeActualSolution()