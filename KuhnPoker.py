from enum import Enum
import itertools

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

        for move in moves:
            res += i * move.value
            i *= 10

        if (len(moves) < 3):
            res += i * Moves.uplayed.value

        return res

    @staticmethod
    def GetInfostate(moves):
        infoSet = KuhnPoker.JoinMoves(moves)
        return infoSet

    def AddToPayoffTable(self, result, moves):
        infoSet = KuhnPoker.GetInfostate(moves)
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
        self.cards = list(CARDS)

    def IsTerminateState(self, infoSet):
        return infoSet in self.payoffTable[infoSet]

    def GetPlayerOnePayoff(self, cardOne, cardTwo, infoSet):
        if(cardOne == cardTwo):
            raise ValueError("The same cards")

        result = self.payoffTable[infoSet]
        if(result[0] == Results.toPlayer1):
            return result[1]
        elif(result[0] == Results.toPlayer2):
            return -result[1]
        else:
            if(cardOne > cardTwo):
                return result[1]
            else:
                return -result[1]

    def NexDeck(self):
        yield itertools.permutations(self.cards)

    def NewRound(self):
        self.cards = self.NexDeck()

 



