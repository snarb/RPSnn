from KuhnPoker import *
import Utils

class CfrNode:
    def __init__(self, infoset):
        self.regretSum = [0.0] * NUM_ACTIONS
        self.nextRegretSum = [0.0] * NUM_ACTIONS
        self.util = [0.0] * NUM_ACTIONS
        self.strategy = [0.0] * NUM_ACTIONS
        self.strategySum = [0.0] * NUM_ACTIONS
        self.infoset = infoset

        self.utilsCount = 0
        self.TotalUtil = 0

        self.avgStrategies = []

    def GetUtilRegretStrategy(self):

        utilsSum = 0
        for action in range(NUM_ACTIONS):
            utilsSum += self.util[action]

        for action in range(NUM_ACTIONS):
            regret = self.util[action] - utilsSum
            self.util[action] = 0
            self.regretSum[action] += regret

        # normalizingSum = np.sum(self.regretSum)
        # if (normalizingSum == 0):
        #     self.strategy = [1.0 / NUM_ACTIONS] * NUM_ACTIONS
        # else:
        #     self.strategy = self.regretSum / normalizingSum
        #
        # return self.strategy

        normalizingSum = 0
        for a in range(NUM_ACTIONS):
            self.strategy[a] = self.regretSum[a] if self.regretSum[a] > 0 else 0
            normalizingSum += self.strategy[a]

        for a in range(NUM_ACTIONS):
            if (normalizingSum > 0):
                self.strategy[a] /= normalizingSum
            else:
                self.strategy[a] = 1.0 / NUM_ACTIONS

            self.strategySum[a] += self.strategy[a]

        return self.strategy


    def GetUtilStrategy(self):

        utilsSum = 0
        for action in range(NUM_ACTIONS):
            utilsSum += self.util[action]

        for a in range(NUM_ACTIONS):
            self.strategy[a] = self.util[action] / utilsSum

        return self.strategy

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

        self.avgStrategies.append(self.GetAverageStrategy())
        return self.strategy

    def GetMegaAvgStrategy(self):
        miss = int(len(self.avgStrategies) * 0.5)
        ar = np.array(self.avgStrategies[miss:])
        mn = np.mean(ar, axis=0)
        return mn

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
