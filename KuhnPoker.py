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

#list(map(int, Color))
MovesToOneHot = {0: 0, 1: 1, 2: 11}
CardsToOneHot = {1: 0, 2: 1, 3: 11}


NUM_ACTIONS = 2

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
        res = ";".join(move.name for move in moves)
        return res

    def AddToPayoffTable(self, result, moves):
        movesStr = KuhnPoker.JoinMoves(moves)
        self.payoffTable[movesStr] = result

    def InitPayoffTable(self):
        self.AddToPayoffTable([Results.toHighCard, 1], [Moves.pas, Moves.pas, Moves.uplayed])
        self.AddToPayoffTable([Results.toPlayer2, 1],  [Moves.pas, Moves.bet, Moves.pas])
        self.AddToPayoffTable([Results.toHighCard, 2], [Moves.pas, Moves.bet, Moves.bet])
        self.AddToPayoffTable([Results.toPlayer1, 1],  [Moves.bet, Moves.pas, Moves.uplayed])
        self.AddToPayoffTable([Results.toHighCard, 2], [Moves.bet, Moves.bet, Moves.uplayed])

    def InitMovesSet(self):
        self.moves =  np.array([Moves.uplayed.value, Moves.uplayed.value, Moves.uplayed.value])
        self.currentMoveId = 0

    def __init__(self):
        self.PayoffCount = 0
        self.payoffTable = {}
        self.InitPayoffTable()
        self.InitMovesSet()

        self.cardsPermutations = []
        for deck in itertools.permutations(CARDS):
            self.cardsPermutations.append(deck)

        self.permutationIndex = 0
        self.cards = None

    # def GetFullInfoSet(self, player):
    #     card = self.GetPlayerCard(player)
    #     for i in range(self.C)
    #
    # def GetPrettyInfoset(self):
    #     target = self.infoSet
    #     for action in Moves:
    #         target = target.replace(action.value, action)
    #
    #     return target

    def MovesToStr(self, movesValuesArray):
        return KuhnPoker.JoinMoves([Moves(move) for move in movesValuesArray])

    def _getInfoset(self, moves, curPlayer):
        card = self.GetPlayerCard(curPlayer)
        infosetString = str(card) + " | " + self.MovesToStr(moves)
        return infosetString

    def GetInfoset(self, curPlayer):
        return self._getInfoset(self.moves, curPlayer)

    def GetLastSubState(self, curPlayer):
        if (curPlayer == Players.one):
            if(self.currentMoveId == 0):
                return str(self.GetPlayerCard(curPlayer))
            elif(self.currentMoveId == 2):
                lastMove = self.moves[self.currentMoveId - 1]
                return str(Moves(lastMove).name)
            else:
                raise ValueError("Call in incorrect currentMoveId")
        else:
             if (self.currentMoveId == 1):
                 lastMove = self.moves[self.currentMoveId - 1]
                 lastMoveStr = self._getInfoset([lastMove], curPlayer)
                 return lastMoveStr
             else:
                raise ValueError("Call in incorrect currentMoveId")

    def GetPrevInfoset(self, curPlayer):
        prevInfoset = self.moves.copy()

        if (curPlayer == Players.one):
            if(self.currentMoveId == 0):
                return "GameTree"
            if(self.currentMoveId == 2):
                prevInfoset[self.currentMoveId - 1] = Moves.uplayed.value
                prevInfoset[self.currentMoveId - 2] = Moves.uplayed.value
            else:
                raise ValueError("Call in incorrect currentMoveId")

        else:
            if (self.currentMoveId == 1):
                return "GameTree"
            else:
                raise ValueError("Call in incorrect currentMoveId")

        return self._getInfoset(prevInfoset, curPlayer)

    def GetPlayerCard(self, player):
        if(not self.cards):
            raise ValueError("Round not started")

        if (player == Players.one):
            return self.cards[0]
        else:
            return self.cards[1]

    def SaveInfoSet(self):
        infosetBackup = self.moves.copy()
        pokerEngineMoveId = self.currentMoveId
        return infosetBackup, pokerEngineMoveId

    def RestoreInfoSet(self, backupTuple):
        self.moves = backupTuple[0].copy()
        self.currentMoveId = backupTuple[1]

    def GetPlayerOneCard(self):
        return self.cards[0]

    def GetCurrentPlayer(self):
        playerId = (self.currentMoveId % 2) + 1
        return Players(playerId)

    def GetPlayerTwoCard(self):
        return self.cards[1]

    def IsTerminateState(self):
        moves = self.MovesToStr(self.moves)
        return moves in self.payoffTable

    def GetPayoff(self, player):
        self.PayoffCount += 1

        cardOne = self.GetPlayerOneCard()
        cardTwo = self.GetPlayerTwoCard()

        if(cardOne == cardTwo):
            raise ValueError("The same cards")

        movesStr = self.MovesToStr(self.moves)
        result = self.payoffTable[movesStr]

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
        self.cards = self.cardsPermutations[self.permutationIndex]
        self.permutationIndex += 1
        if(self.permutationIndex >= len(self.cardsPermutations)):
            self.permutationIndex = 0
            retValue = 1

        #self.cards = self.cardsPermutations[len(self.cardsPermutations) - 1] #ToDO: REMOVE!!!!!! Temp!!!!!!
        self.InitMovesSet()
        return retValue


    def MakeMove(self, move):
        self.MakeOneHotMove(move.value)

    def MakeOneHotMove(self, adHocMove):
        if (not self.cards):
            raise ValueError("Round not started")

        if(self.currentMoveId >= len(self.moves)):
            ValueError("To much moves!")

        self.moves[self.currentMoveId] = adHocMove
        self.currentMoveId += 1



