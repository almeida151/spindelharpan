import random 

def generateDeck(randomDeck = True, deckType = 'normal'):

    cardList = []

    if (deckType == 'normal'):
        for suitIter in range(4):
            for valueIter in range(1,14):
                cardList.append(Card(valueIter, suitIter))
    if (deckType == 'double'):
        for suitIter in range(4):
            for valueIter in range(1,14):
                cardList.append(Card(valueIter, suitIter))
                cardList.append(Card(valueIter, suitIter))

    if (deckType == 'double-one-color'):
        for suitIter in [0,0,0,0]:
            for valueIter in range(1,14):
                cardList.append(Card(valueIter, suitIter))
                cardList.append(Card(valueIter, suitIter))
    if (deckType == 'double-two-color'):
        for suitIter in [0,0,1,1]:
            for valueIter in range(1,14):
                cardList.append(Card(valueIter, suitIter))
                cardList.append(Card(valueIter, suitIter))
    if (deckType == 'quarter-one-color'):
        for valueIter in range(1,14):
            cardList.append(Card(valueIter, 0))

    if randomDeck:
        random.shuffle(cardList)

    return cardList

class Card:
    suitNames = ['S', 'H', 'D', 'C']

    def __init__(self, value, suit):
        # 0, 1, 2, 3 is spades, hearts, diamonds and clubs respectivly
        self.suit = suit
        self.value = value

    def __repr__(self):
        rv = '|'
        if (self.value == 1):
            rv += 'A'
        elif (self.value == 11):
            rv += 'J'
        elif (self.value == 12):
            rv += 'Q'
        elif (self.value == 13):
            rv += 'K'
        else:
            rv += str(self.value)

        rv += ' of ' + self.suitNames[self.suit] + '|'

        return f"{rv:^10}"

