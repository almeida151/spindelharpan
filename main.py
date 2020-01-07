from QPlayer import QPlayer
from SpindelTable import Table
import json
import itertools
import matplotlib.pyplot as plt



# Run 100 games 
wonGames = 0
N = 100
qPlayer = QPlayer(None, loadFromFile = False)
won = []

for i in range(N):
    print("Game: " + str(i))

    table = Table(1)
    qPlayer.newTable(table)
    qPlayer.gambleChance -= 1/N
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
        print(f"            WON ({wonGames} of {i})")
        won.append(1)
    else:
        print(f"             lost(won {wonGames} of {i})")
        won.append(0)

print(f"Number of won games: {wonGames} out of {N}")
cumsum = list(itertools.accumulate(won))
plt.plot(cumsum)
plt.show()
plt.savefig("out.png")



