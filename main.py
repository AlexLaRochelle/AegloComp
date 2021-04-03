from commande import Commande
from entrepot import Entrepot
from grid import Grid
from position import Position


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    challenge_file = open('maps/busy_day.in', 'r')

    setup_line = challenge_file.readline()
    setup_numbers = setup_line.split(' ')
    grid = Grid(setup_numbers[0], setup_numbers[1])

    productAmount = challenge_file.readline()
    products_weights = challenge_file.readline().split(' ')
    products_weights = [int(numeric_string) for numeric_string in products_weights]
    #print(products)

    entrepotsAmount = int(challenge_file.readline())
    entrepots = []

    for entrepotId in range(entrepotsAmount):
        entrepotPosEntry = challenge_file.readline().split(' ')
        entrepotProductsEntry = challenge_file.readline().split(' ')
        entrepotProductsEntry = [int(numeric_string) for numeric_string in entrepotProductsEntry]

        entrepots.append(Entrepot(Position(int(entrepotPosEntry[0]), int(entrepotPosEntry[1])), entrepotProductsEntry))


    #print(entrepots)

    commandesAmount = int(challenge_file.readline())
    commandes = []

    for commandeId in range(commandesAmount):
        commandePosEntry = challenge_file.readline().split(' ')
        commandeProductsAmount = challenge_file.readline()
        commandeAllProducts = challenge_file.readline().split(' ')
        commandeAllProducts = [int(numeric_string) for numeric_string in commandeAllProducts]

        commandes.append(Commande(Position(int(commandePosEntry[0]), int(commandePosEntry[1])), commandeAllProducts))

    #print(commandes)


