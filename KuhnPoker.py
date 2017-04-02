from enum import Enum
import itertools

class Players(Enum):
    one = 1
    two = 2

class Moves(Enum):
    uplayed = 0
    pas = 1
    bet = 2

class Results(Enum):
    toHighCard = 0
    toPlayer1 = 1
    toPlayer2 = 2

CARDS = [1, 2, 3]

class KuhnPoker:
    @staticmethod
    def JoinMoves(moves):
        res = 0
        i = 1

        for move in reversed(moves):
            res += i * move.value
            i *= 10

        if (len(moves) < 3):
            res += i * Moves.uplayed.value

        return res

    @staticmethod
    def GetInfoSet(moves):
        infoSet = KuhnPoker.JoinMoves(moves)
        return infoSet

    def AddToPayoffTable(self, result, moves):
        infoSet = KuhnPoker.GetInfoSet(moves)
        self.payoffTable[infoSet] = result

    def InitPayoffTable(self):
        self.AddToPayoffTable([Results.toHighCard, 1], [Moves.pas, Moves.pas])
        self.AddToPayoffTable([Results.toPlayer2, 1],  [Moves.pas, Moves.bet, Moves.pas])
        self.AddToPayoffTable([Results.toHighCard, 2], [Moves.pas, Moves.bet, Moves.bet])
        self.AddToPayoffTable([Results.toPlayer1, 1],  [Moves.bet, Moves.pas])
        self.AddToPayoffTable([Results.toHighCard, 2], [Moves.bet, Moves.bet])

    def __init__(self):
        self.payoffTable = {}
        self.InitPayoffTable()
        self.infoSet = None

        self.cardsPermutations = []
        for deck in itertools.permutations(CARDS):
            self.cardsPermutations.append(deck)

        self.permutationIndex = 0
        self.cards = self.cardsPermutations[0]

    def GetPlayerOneCard(self):
        return self.cards[0]

    def GetPlayerTwoCard(self):
        return self.cards[1]

    def IsTerminateState(self):
        return self.infoSet in self.payoffTable

    def GetPayoff(self, player):
        cardOne = self.GetPlayerOneCard()
        cardTwo = self.GetPlayerTwoCard()

        if(cardOne == cardTwo):
            raise ValueError("The same cards")

        result = self.payoffTable[self.infoSet]

        winner = result[0]
        reward = result[1]

        if(player == Players.two):
            reward = reward * (-1);

        if(winner == Results.toPlayer1):
            return reward
        elif(winner == Results.toPlayer2):
            return -reward
        else:
            if(cardOne > cardTwo):
                return reward
            else:
                return -reward

    def _nexDeck(self):
        for deck in itertools.permutations(CARDS):
            yield deck

    def NewRound(self):
        self.permutationIndex += 1
        if(self.permutationIndex >= len(self.cardsPermutations)):
            self.permutationIndex = 0

        self.cards = self.cardsPermutations[self.permutationIndex]

    def MakeMove(self, move):
        if (not self.infoSet):
            self.infoSet = move.value
        else:
            self.infoSet *= 10
            self.infoSet += move.value


# kn = KuhnPoker()
# kn.NewRound()
# kn.NewRound()
#
# kn.MakeMove(Moves.pas)
# print(kn.infoSet)
# kn.MakeMove(Moves.bet)
# print(kn.infoSet)
#
# kn.MakeMove(Moves.bet)
# print(kn.infoSet)
#
# rr = kn.IsTerminateState()
# ff = kn.GetPayoff(Players.one)
# print(ff)