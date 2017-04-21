from KuhnPoker import *

class CfrNode:
    def __init__(self, infoset):
        self.regretSum = [0.0] * NUM_ACTIONS
        self.strategy = [0.0] * NUM_ACTIONS
        self.strategySum = [0.0] * NUM_ACTIONS
        self.infoset = infoset

    def GetStrategy(self, realizationWeight):
        normalizingSum = 0
        for a in range(NUM_ACTIONS):
            self.strategy[a] = self.regretSum[a] if self.regretSum[a] > 0 else 0
            normalizingSum += self.strategy[a]

        for a in range(NUM_ACTIONS):
            if (normalizingSum > 0):
                self.strategy[a] /= normalizingSum
            else:
                self.strategy[a] = 1.0 / NUM_ACTIONS
                self.strategySum[a] += realizationWeight * self.strategy[a]

        return self.strategy

    def GetAverageStrategy(self):
        avgStrategy = [0.0] * NUM_ACTIONS

        normalizingSum = 0
        for a in range(NUM_ACTIONS):
            normalizingSum += self.strategySum[a]

        for a in range(NUM_ACTIONS):
            if (normalizingSum > 0):
                avgStrategy[a] = self.strategySum[a] / normalizingSum
            else:
                avgStrategy[a] = 1.0 / NUM_ACTIONS
        return avgStrategy

    def __str__(self):
        return str(self.strategySum) + " | " + str(self.regretSum)
