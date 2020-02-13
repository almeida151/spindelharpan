from QPlayer import QPlayer
from SpindelTable import Table
from Deck import generateDeck
import json
import itertools
import matplotlib.pyplot as plt
import random



# Run 100 games 
wonGames = 0
N = 1000
qPlayer = QPlayer(None, loadFromFile = True)
qPlayer.gambleChance = 0.3

won = []

for i in range(N):
    print("Game: " + str(i))

    table = Table(-1)
    deck = generateDeck(True, 'quarter-one-color')
    for randStackNo in (random.randint(0,9) for i in range(13)):
        table.stacks[randStackNo].faceUpCards.append(deck.pop())

    qPlayer.newTable(table)
    qPlayer.gambleChance -= 0.3/N
    lastPile = False

    # Game loop
    while True:

        # distribute loop
        n = 0
        while True:

            # Prevent going too many moves
            n += 1
            if n > 200:
                break

            # Print every something
            if not n % 1000:
                pass
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

# Save the Q matrix in a json file
jsonDump = json.dumps(qPlayer.Q)
f = open("Q.json","w")
f.write(jsonDump)
f.close()

# Make graph over won games
print(f"Number of won games: {wonGames} out of {N}")
cumsum = list(itertools.accumulate(won))
movingaverage = [sum(won[n:n+int(N/10)])/int(N/10) for n in range(N-int(N/10))]
plt.plot(range(int(N/10), N), movingaverage)
plt.show()
plt.savefig("out.png")



