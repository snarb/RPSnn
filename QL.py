import Utils
import random

from KuhnPoker import *
from treelib import Node, Tree
from CfrNode import CfrNode
from GameTree import GameTree
from matplotlib import pyplot as plt
from Qlnode import Qlnode

class QLtrainer:
    ALPHA = 0.05
    BETA = 0.001

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
        infosetBackup = self.kuhn.SaveInfoSet()


        if (random.random() < QLtrainer.BETA):
            strategy = np.array([0.5] * NUM_ACTIONS)
        else:
            strategy = dataNode.strategies

        action = Utils.MakeChoise(strategy, 1)[0]
        self.kuhn.MakeAction(action)

        if (curPlayer == Players.one):
            util = -self.GetNodeValue(p0 * strategy[action], p1)
        else:
            util = -self.GetNodeValue(p0, p1 * strategy[action])

        strategy[action] *= (1 + util * QLtrainer.ALPHA * curPlayerProb) # ToDo: Gradient? Gradient of regret? Do I need * curPlayerProb???!!!
        dataNode.strategies = Utils.Normalise(strategy)

        self.kuhn.RestoreInfoSet(infosetBackup)

        return util


    def Train(self):
        util = 0
        cnt = 0
        results = []

        for i in range(1, 1000):
            self.kuhn.NewRound()
            util += self.GetNodeValue(1, 1)
            if(cnt % 100 == 0):
                results.append(util / i)

        print("Avg util:", util / i)
        plt.plot(results)
        plt.show()




trainer = QLtrainer()
trainer.Train()

# print("Player one avg strategy:")
# trainer.playerOneTree.PrintAvgStrategy()
# print("Player one best resp strategy:")
# trainer.playerOneTree.PrintBestResp()
# print("Player one regrets:")
# trainer.playerOneTree.PrintRegrets()
#
#
# print("----------------------")
# print("Player two avg strategy:")
# trainer.playerTwoTree.PrintAvgStrategy()
# print("Player two best resp strategy:")
# trainer.playerTwoTree.PrintBestResp()
# print("Player two regrets:")
# trainer.playerTwoTree.PrintRegrets()


print("done")