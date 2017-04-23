import Utils
import random

from KuhnPoker import *
from treelib import Node, Tree
from CfrNode import CfrNode
from GameTree import GameTree
from matplotlib import pyplot as plt
from Qlnode import Qlnode

class QLtrainer:
    ALPHA = 1
    BETA = 0.05
    SAMPLE_SIZE = 10

    def __init__(self):
        self.playerOneTree = GameTree(Qlnode)
        self.playerTwoTree = GameTree(Qlnode)
        self.kuhn = KuhnPoker()

    def GetNodeValue(self, p0, p1):
        curPlayer = self.kuhn.GetCurrentPlayer()

        if (self.kuhn.IsTerminateState()):
            return self.kuhn.GetPayoff(curPlayer)

        curPlayerProb = p0 if curPlayer == Players.one else p1
        tree = self.playerOneTree if curPlayer == Players.one else self.playerTwoTree
        dataNode = tree.GetOrCreateDataNode(self.kuhn, curPlayer)

        infosetStr = self.kuhn.GetInfoset(curPlayer)
        if (random.random() < QLtrainer.BETA):
            strategy = np.array([0.5] * NUM_ACTIONS)
        else:
            strategy = dataNode.strategy

        sampleSize = max(int(round(QLtrainer.SAMPLE_SIZE * p0 * p1)), 1)

        actions = Utils.MakeChoise(strategy, sampleSize)

        util = [0.0] * NUM_ACTIONS
        nodeUtil = 0

        infosetBackup = self.kuhn.SaveInfoSet()

        for action in actions:

            self.kuhn.MakeAction(action)

            if (curPlayer == Players.one):
                util[action] = -self.GetNodeValue(p0 * strategy[action], p1)
            else:
                util[action] = -self.GetNodeValue(p0, p1 * strategy[action])

            nodeUtil += strategy[action] * util[action]

            self.kuhn.RestoreInfoSet(infosetBackup)

        regrets = [0.0] * NUM_ACTIONS

        for action in range(NUM_ACTIONS):
            regret = util[action] - nodeUtil
            opProb = p1 if curPlayer == Players.one else p0
            #cfrNode.regretSum[action] += opProb * regret
            regrets[action] = regret * opProb
            #strategy[action] *= (1 + util * QLtrainer.ALPHA * curPlayerProb) # ToDo: Gradient? Gradient of regret? Do I need * curPlayerProb???!!!
            #strategy[action] +=  regret * QLtrainer.ALPHA * opProb # ToDo: Gradient? Gradient of regret? Do I need * curPlayerProb???!!!
            #strategy[action] = max(strategy[action], 0)

        regrets= Utils.Normalise(regrets)

        dataNode.strategy = Utils.Normalise(strategy)



        return nodeUtil / len(actions)


    def Train(self):
        util = 0
        cnt = 0
        results = []

        for i in range(1, 1000):
            self.kuhn.NewRound()
            util += self.GetNodeValue(1, 1)
            if(cnt % 100 == 0):
                results.append(util / i)

            # QLtrainer.ALPHA *= 0.999
            # QLtrainer.BETA *= 0.999

        print("Avg util:", util / i)
        # print(QLtrainer.ALPHA, QLtrainer.BETA)
        plt.plot(results)
        plt.show()




trainer = QLtrainer()
trainer.Train()



print("Player one strategy:")
trainer.playerOneTree.PrintStrategy()

print("Player two strategy:")
trainer.playerTwoTree.PrintStrategy()


print("done")