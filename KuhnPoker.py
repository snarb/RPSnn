from enum import Enum
from queue import *
import numpy as np
import itertools

class Players(Enum):
    one = 1
    two = 2

class Moves(Enum):
    uplayed = 0
    pas = 1
    bet = 11

MovesToOneHot = {0: 0, 1: 1, 2: 11}
CardsToOneHot = {1: 0, 2: 1, 3: 11}

class Results(Enum):
    toHighCard = 0
    toPlayer1 = 1
    toPlayer2 = 2

CARDS = [1, 2, 3]

def NextPlayer(currentPlayer):
    if(currentPlayer == Players.one):
        return Players.two

    return Players.one

class KuhnPoker:
    @staticmethod
    def JoinMoves(moves):
        res = np.array_str(moves)
        return res

    @staticmethod
    def GetInfoSet(moves):
        infoSet = KuhnPoker.JoinMoves(moves)
        return infoSet

    def AddToPayoffTable(self, result, moves):
        infoSet = KuhnPoker.GetInfoSet(np.array([move.value for move in moves]))
        self.payoffTable[infoSet] = result

    def InitPayoffTable(self):
        self.AddToPayoffTable([Results.toHighCard, 1], [Moves.pas, Moves.pas, Moves.uplayed])
        self.AddToPayoffTable([Results.toPlayer2, 1],  [Moves.pas, Moves.bet, Moves.pas])
        self.AddToPayoffTable([Results.toHighCard, 2], [Moves.pas, Moves.bet, Moves.bet])
        self.AddToPayoffTable([Results.toPlayer1, 1],  [Moves.bet, Moves.pas, Moves.uplayed])
        self.AddToPayoffTable([Results.toHighCard, 2], [Moves.bet, Moves.bet, Moves.uplayed])

    def InitInfoSet(self):
        self.infoSet =  np.array([Moves.uplayed.value, Moves.uplayed.value, Moves.uplayed.value])
        self.currentMoveId = 0

    def __init__(self):
        self.PayoffCount = 0
        self.payoffTable = {}
        self.InitPayoffTable()
        self.InitInfoSet()

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
        return self.GetStringInfoset() in self.payoffTable

    def GetStringInfoset(self):
        return np.array_str(self.infoSet)

    def GetPayoff(self, player):
        self.PayoffCount += 1

        cardOne = self.GetPlayerOneCard()
        cardTwo = self.GetPlayerTwoCard()

        if(cardOne == cardTwo):
            raise ValueError("The same cards")

        result = self.payoffTable[self.GetStringInfoset()]

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
        retValue = 0

        self.permutationIndex += 1
        if(self.permutationIndex >= len(self.cardsPermutations)):
            self.permutationIndex = 0
            retValue = 1

        self.cards = self.cardsPermutations[self.permutationIndex]
        self.InitInfoSet()
        return retValue


    def MakeMove(self, move):
        self.MakeOneHotMove(move.value)

    def MakeOneHotMove(self, adHocMove):
        if(self.currentMoveId >= len(self.infoSet)):
            ValueError("To much moves!")

        self.infoSet[self.currentMoveId] = adHocMove
        self.currentMoveId += 1



