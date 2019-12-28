import Deck 
import random

class CardStack:
    # A stack of cards with some face up and some face down. To be used in the game Spindelharpan

    def __init__(self):
        # Initializes list of face down and face up cards
        self.faceDownCards = []
        self.faceUpCards = []

    def flipCard(self):
        # Flips a card from bein face down to being face up. 
        # Can only be done when there are no face up cards in the stack
        # If there are no face down cards to be flipped, it does nothing. 

        if self.faceUpCards:
            raise RuntimeError("Called flipCard in an inappropriate situation")

        if self.faceDownCards:
            self.faceUpCards.append(self.faceDownCards.pop())


    def popTop(self):
        # Removes and returns the top card of the face up pile
        # Trows error if there are no face up cards

        returnCard = self.faceUpCards.pop()

        if not faceUpCards:
            self.flipCard()

        return returnCard

    def numberOfMovable(self):
        # Returns how many cards can be moved. 
        # The rule is that if a set of cards is of the same suit and in a 
        # decending straight (lower values in front) they can be moved as one

        if not self.faceUpCards:
            return 0

        rv = 0
        topSuit = self.faceUpCards[-1].suit
        topValue = self.faceUpCards[-1].value

        i = 2
        while True:
            try:
                if topSuit != self.faceUpCards[-i].suit:
                    break
                elif topValue != self.faceUpCards[-i].value + 1-i:
                    break
            except IndexError:
                break
            i += 1

        return i-1

    def __repr__(self):
        rv = ""
        for card in self.faceDownCards:
            rv += repr(card)
            rv += "(hidden)\n"
        for card in self.faceUpCards:
            rv += repr(card)
            rv += "\n"
        return rv



class Table:

    def __init__(self, noOfColors):

        if noOfColors == 1:
            deck = Deck.generateDeck(deckType='double-one-color')
        elif noOfColors == 2:
            deck = Deck.generateDeck(deckType='double-two-color')
        elif noOfColors == 4:
            deck = Deck.generateDeck(deckType='double')
        else:
            print(str(noOfColors) + 'is not a valid color')

        self.timesDistributed = 0
        self.piles = []
        for i in range(5):
            self.piles.append(deck[-10:])
            del deck[-10:]

        self.stacks = []
        for i in range(10):
            cardStack = CardStack()
            if i < 4:
                cardStack.faceDownCards = deck[-6:]
                del deck[-6:]
            else:
                cardStack.faceDownCards = deck[-5:]
                del deck[-5:]
            cardStack.flipCard()

            self.stacks.append(cardStack)

    def move(self, stackNumberFrom, stackNumberTo, numberOfCards=1):
        # Moves numberOfCards from one stack to another, if it is possible
        # If the move results in a straight from king to ace, it is removed

        #Check if the stacknumbers are valid
        if stackNumberTo > 9 or stackNumberFrom > 9 or stackNumberTo < 0 or stackNumberFrom < 0:
            print("Invalid stacknumber")
            return

        # Check if the numberOfCards is valid
        if self.stacks[stackNumberFrom].numberOfMovable() < numberOfCards:
            print("Too many cards to be moved, not allowed")
            return

        # Check if the move is possible
        valueMoved = self.stacks[stackNumberFrom].faceUpCards[-numberOfCards].value
        try:
            valueTo = self.stacks[stackNumberTo].faceUpCards[-1].value
        except IndexError:
            # Stack moved to is empty
            pass
        else:
            # No exception: stack moved to is not empty
            if  valueMoved + 1 != valueTo:
                print(f"Not a legal move: valueMoved: {valueMoved}, valueTo: {valueTo}, stackFrom: {stackNumberFrom}, stackTo: {stackNumberTo}, numberOfCards: {numberOfCards}")
                return

        # Move the move
        cardsToBeMoved = self.stacks[stackNumberFrom].faceUpCards[-numberOfCards:]
        del self.stacks[stackNumberFrom].faceUpCards[-numberOfCards:]
        self.stacks[stackNumberTo].faceUpCards.extend(cardsToBeMoved)

        # If that moved all of the face up cards, flip the pile
        if not self.stacks[stackNumberFrom].faceUpCards:
            self.stacks[stackNumberFrom].flipCard()

        # If that made a straight from King to Ace, remove them
        if self.stacks[stackNumberTo].numberOfMovable() == 13:
            print("YEEEHAAA")
            del self.stacks[stackNumberTo].faceUpCards[-13:]

        # If that removed all of the face up cards, flip the pile
        if not self.stacks[stackNumberTo].faceUpCards:
            self.stacks[stackNumberTo].flipCard()

    def possibleMoves(self):
        # Returns all possible moves in the form (stackNumberFrom, stackNumberTo, numberOfCards)

        listOfPossibleMoves = []

        # A list of the values we can move TO
        topValues = [card.value if card is not None else -1 for card in self.getTopCards()]

        # For each stack, check all possible moves from that stack to see if they can be put on another stack
        for stackNumberFrom in range(len(self.stacks)):
            numberOfMovable = self.stacks[stackNumberFrom].numberOfMovable()

            for i in range(1,numberOfMovable+1):
                valueFrom = self.stacks[stackNumberFrom].faceUpCards[-i].value
                #   Add all values that are one more than the value moved.
                stackNumberTos = [index for index, value in enumerate(topValues) if value == valueFrom +1]
                #   Add all stacks that are empty
                stackNumberTos.extend([index for index, value in enumerate(topValues) if value == -1])

                listOfPossibleMoves.extend([(stackNumberFrom,stackNumberTo,i) for stackNumberTo in stackNumberTos])

        return listOfPossibleMoves

    def getTopCards(self):
        rv = []
        for cardStack in self.stacks:
            try:
                rv.append(cardStack.faceUpCards[-1])
            except IndexError:
                rv.append(None)

        return rv


    def distribute(self):
        if not self.piles:
            print("No more piles to distribute")
            return
        pile = self.piles.pop()
        for cardStack in self.stacks:
            cardStack.faceUpCards.append(pile.pop())

        self.timesDistributed += 1

    def isWon(self):
        # Returns true if there are no cards on the table
        won = True
        for cardStack in self.stacks:
            if cardStack.faceDownCards or cardStack.faceUpCards:
                won = False
        return won

    def __repr__(self):
        rvarr = []

        maxLen = 0
        for cardStack in self.stacks:
            stackLength = len(cardStack.faceDownCards) + len(cardStack.faceUpCards)
            if stackLength > maxLen:
                maxLen = stackLength

        rvarr = [[" "*10]*10]*(maxLen)
        rvarr = [row.copy() for row in rvarr]


        for i in range(len(self.stacks)):
            j = 0
            for _ in range(len(self.stacks[i].faceDownCards)):
                rvarr[j][i] = f"{'|hidden|':^10}"
                j += 1
            for k in range(len(self.stacks[i].faceUpCards)):
                rvarr[j+k][i] = repr(self.stacks[i].faceUpCards[k])

        # Insert row numbers
        rvarr.insert(0,[f"{str(i):^10}" for i in range(10)])

        rv = "\n".join(["".join(row) for row in rvarr])
        return rv




