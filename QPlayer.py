import random
import itertools
import json

class QPlayer:

    # Like an overall gas pedal, not too high or you'll miss the optimum,
    # not too low or you'll never get there
    learningRate = 0.1
    # Kind of decides how much to value future rewards in comparison to present ones
    discount = 0.95 
    # What are the chances to randomize movement
    gambleChance = 1

    def __init__(self, t, _Q = None, loadFromFile = False):
        # Initialize Q matrix as empty dictionary
        # Q keys are [n,m,s,h1,h2,[2,5,2,1],[3,2,2]]
        # 
        # Meanings: n - number of distributes left,
        # m - number of cards to be moved
        # s - boolean, is suit moved to and from the same
        # h1, h2 - number of hidden cards in from and to
        # arrays - number of connected cards in from and to
        #           i.e. K,Q,J,3,5,4 would get [3,1,2] (if all in same suit)
        if not loadFromFile:
            self.Q = {} if _Q is None else _Q
        else:
            with open("Q.json") as f:
                self.Q = json.load(f)

        self.table = t

    def reward(self, move):
        # Reward 100 if move results in a stack of king to ace
        # Reward 1 if move results in flip of hidden card
        # Reward for creating empty stack unless moving to empty stack
        reward = 0

        if len(move) == 2:
            move.append(1)
        # If lowest of moved stack is an ace, and the card to be [-13] is king
        if len(self.table.stacks[move[1]].faceUpCards) >= 13-move[2]:
            if self.table.stacks[move[0]].faceUpCards[-1].value == 1 \
               and self.table.stacks[move[1]].faceUpCards[-(13-move[2])].value == 13:
                reward += 100

        # If move results in a card flipped or empty stack created
        if len(self.table.stacks[move[0]].faceUpCards) == move[2]:
            # If move is not to empty stack
            if self.table.stacks[move[1]].faceUpCards:
                reward += 1

        return reward

    def moveToQKey(self, move):
        n = self.table.timesDistributed
        m = move[2] if len(move) == 3 else 1
        h1 = len(self.table.stacks[move[0]].faceDownCards)
        h2 = len(self.table.stacks[move[1]].faceDownCards)

        # The move to stack could be empty
        if self.table.stacks[move[1]].faceUpCards:
            s = self.table.stacks[move[0]].faceUpCards[-1].suit == \
                self.table.stacks[move[1]].faceUpCards[-1].suit
        else:
            s = False

        arrFrom = []
        counter = 0
        # Loop over cards from bottom to top.
        for card in self.table.stacks[move[0]].faceUpCards:
            counter += 1
            if counter == 1:
                prevCard = card
                continue
            # If this card does not fit with the previous card, reset the counter
            # And append to arrFrom how many cards fit before one was found that didn't
            if card.suit != prevCard.suit or card.value +1 != prevCard.value:
                arrFrom.append(counter -1)
                counter = 0

            prevCard = card

        # Append the last sequence
        if counter:
            arrFrom.append(counter)

        arrTo = []
        counter = 0
        # Loop over cards from bottom to top.
        for card in self.table.stacks[move[1]].faceUpCards:
            counter += 1
            if counter == 1:
                continue
            # If this card does not fit with the previous card, reset the counter
            # And append to arrFrom how many cards fit before one was found that didn't
            if card.suit != prevCard.suit or card.value +1 != prevCard.value:
                arrTo.append(counter -1)
                counter = 0
            prevCard = card

        # Append the last sequence
        if counter:
            arrTo.append(counter)

        qKey = [n,m,s,h1,h2,arrFrom,arrTo]
        return str(qKey)

    def move(self):
        # Makes a move, cannot be distribute

        possMoves = self.table.possibleMoves()

        # If there are no moves, just return
        if not possMoves:
            return

        # Convert move to qKey, the different qKeys correspond to a state action pair
        qKeys = [self.moveToQKey(move) for move in possMoves]
        # For each key in qKeys, get the corresponding value from the Q matrix
        # If there is none, get 0
        qValues = [self.Q[qKey] if qKey in self.Q else 0 for qKey in qKeys]


        # Select a move

        # should we gamble?
        gamble = random.random() < self.gambleChance

        # Choose a move weighted with the q values
        if gamble:
            try:
                minPosQValue = min([qValue for qValue in qValues if qValue > 0])
            except ValueError:
                # No nonzero qValues
                minPosQValue = 1

            # Add min positive value / 2 to all values to give those with 0 qvalue a chance
            shiftedQValues = [qValue + minPosQValue/2.0 for qValue in qValues]
            # Normalize
            sumQValues = sum(shiftedQValues)
            shiftedQValues = [shiftedQValue/sumQValues for shiftedQValue in shiftedQValues]

            r = random.random()
            cumsumQValues = itertools.accumulate(shiftedQValues)
            for i in range(len(shiftedQValues)):
                if next(cumsumQValues) >= r:
                    moveIndex = i
                    break
        else:
            # Just choose the maximum
            f = lambda i: qValues[i]
            moveIndex = max(range(len(qValues)), key=f)

        # Save the reward, for use later, when updating the Q matrix
        reward = self.reward(possMoves[moveIndex])

        # Move the move
        move = possMoves[moveIndex]
        self.table.move(*move)
        movedQKey = qKeys[moveIndex]

        # Find the qValues of the newly available moves
        possMoves = self.table.possibleMoves()
        qKeys = [self.moveToQKey(move) for move in possMoves]
        qValues = [self.Q[qKey] if qKey in self.Q else 0 for qKey in qKeys]

        if not(movedQKey in self.Q):
            self.Q[movedQKey] = 0

        # If there are now no available moves, distribute
        if not possMoves:
            if self.table.timesDistributed == 5:
                return -1

            self.table.distribute()

        """
        # If the best move now is to revert the previous move
        # And reverting has a lower q-value than going forward, distribute instead
        if possMoves:
            f = lambda i: qValues[i]
            bestMoveIndex = max(range(len(qValues)), key=f)
            if move[0] == possMoves[bestMoveIndex][1] and \
               move[1] == possMoves[bestMoveIndex][0] and \
               move[2] == possMoves[bestMoveIndex][2] and \
               self.Q[movedQKey] >= qValues[bestMoveIndex] \
               and qValues[bestMoveIndex] != 0:

                if self.table.timesDistributed == 5:
                    return -1
                self.table.distribute()
        """


        # Update the Q matrix
        self.Q[movedQKey] += self.learningRate * (reward + self.discount*max(qValues+[0]) - self.Q[movedQKey])


        return 0

    def newTable(self, t):
        self.table = t


