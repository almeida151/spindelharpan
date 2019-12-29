from QPlayer import QPlayer
from SpindelTable import Table
import json



# Run 100 games 
wonGames = 0
N = 10
qPlayer = QPlayer(None, loadFromFile = True)

for i in range(N):
    print("Game: " + str(i))

    table = Table(1)
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
            if n > 5000 and lastPile:
                break

            # Print every something
            if not n % 1000:
                jsonDump = json.dumps(qPlayer.Q)
                f = open("Q.json","w")
                f.write(jsonDump)
                f.close()
                print(n)

            possMoves = table.possibleMoves()
            if not possMoves:
                break

            qPlayer.move()
            #input("Press Enter to continue...")

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





