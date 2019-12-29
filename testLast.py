from QPlayer import QPlayer
from SpindelTable import Table
import random
import json
from Deck import Card


# Run 100 games 
wonGames = 0
N = 100
qPlayer = QPlayer(None, loadFromFile = False)

for i in range(N):
    print("Game: " + str(i))

    table = Table(1)

    table.piles = []
    for stack in table.stacks:
        stack.faceDownCards = []
        stack.faceUpCards = []
    cards = [Card(1,0),Card(2,0),Card(3,0),Card(4,0),Card(5,0),Card(6,0),Card(7,0),Card(8,0),Card(9,0),Card(10,0),Card(11,0),Card(12,0),Card(13,0)]
    random.shuffle(cards)
    for i in range(13):
        table.stacks[i%10].faceUpCards.append(cards[i])

    print(table)

    qPlayer.newTable(table)
    lastPile = False

    # Game loop
    while True:

        # distribute loop
        n = 0
        while True:

            # Prevent going back and forth
            n += 1
            if n > 1000 and not lastPile:
                break
            if n > 10000 and lastPile:
                break

            # Print every something
            if not n % 1000:
                jsonDump = json.dumps(qPlayer.Q)
                f = open("Q.json","w")
                f.write(jsonDump)
                f.close()
                #print(n)

            possMoves = table.possibleMoves()
            if not possMoves:
                break

            qPlayer.move()
            #input("Press Enter to continue...")

            if table.isWon():
                break

        if table.piles:
            table.distribute()
            print("Distributing")
            if not table.piles:
                lastPile = True
            continue

        break

    if table.isWon():
        wonGames += 1
        print("WON")
    else:
        print("lost")

print(f"Number of won games: {wonGames} out of {N}")

