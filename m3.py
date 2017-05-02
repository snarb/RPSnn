import random
import Utils
import math
from KuhnPoker import *
from treelib import Node, Tree
from CfrNode import CfrNode
from GameTree import GameTree
from matplotlib import pyplot as plt

class CFRtrainer:
    BETA = 0.00
    SAMPLE_SIZE = 24 #16 #24

    def __init__(self):
        self.playerOneTree = GameTree(CfrNode)
        self.playerTwoTree = GameTree(CfrNode)
        self.kuhn = KuhnPoker()

    def CFR(self, curSamplesCount):
        curPlayer = self.kuhn.GetCurrentPlayer()

        if(self.kuhn.IsTerminateState()):
            return self.kuhn.GetPayoff(curPlayer)

        tree = self.playerOneTree if curPlayer == Players.one else self.playerTwoTree
        cfrNode = tree.GetOrCreateDataNode(self.kuhn, curPlayer)
        util = [0.0] * NUM_ACTIONS

        if (random.random() < CFRtrainer.BETA):
            strategy = np.array([0.5] * NUM_ACTIONS)
        else:
            strategy = cfrNode.GetUtilStrategy()

        #CFRtrainer.BETA *= 0.9
        sampleSize = max(int(round(curSamplesCount)), 1)
        nextSamplesCount = math.sqrt(curSamplesCount)

        actions = Utils.MakeChoise(strategy, sampleSize)


        infosetStr = self.kuhn.GetInfoset(curPlayer)
        if(('1 | bet' in infosetStr) and curPlayer == Players.two):
            g = 6
        nodeUtil = 0

        infosetBackup = self.kuhn.SaveInfoSet()

        for action in actions:
            self.kuhn.MakeAction(action)
            util[action] = -self.CFR(nextSamplesCount)
            self.kuhn.RestoreInfoSet(infosetBackup)

        for action in range(NUM_ACTIONS):
            util[action] /= sampleSize #expected util per single sample. Maybe we can remove?
            nodeUtil += util[action]

        # for action in range(NUM_ACTIONS):
        #     if(strategy[action] > 0):
        #         curUtil = util[action]
        #         cfrNode.util[action] += curUtil

        # cfrNode.TotalUtil += nodeUtil
        # cfrNode.utilsCount += 1

        for action in range(NUM_ACTIONS):
            if(strategy[action] > 0):
                maxActionProfit = util[action] / strategy[action]
                regret = maxActionProfit - nodeUtil
                cfrNode.regretSum[action] += regret
            else:
                assert (util[action] == 0)

        return nodeUtil

    def Train(self):
        util = 0
        cnt = 0

        results = []

        for i in range(1, 3000):
            self.kuhn.NewRound()
            util += self.CFR(CFRtrainer.SAMPLE_SIZE)
            if(cnt % 100 == 0):
                results.append(util / i)

        print("Avg util:", util / i)
        plt.plot(results)
        plt.show()



# #
# trainer = CFRtrainer()
# trainer.Train()
# #
# print("Player one avg strategy:")
# trainer.playerOneTree.PrintAvgStrategy()
# # print("Player one best resp strategy:")
# # trainer.playerOneTree.PrintBestResp()
# # print("Player one regrets:")
# # trainer.playerOneTree.PrintRegrets()
# #
# #
# print("----------------------")
# print("Player two avg strategy:")
# trainer.playerTwoTree.PrintAvgStrategy()
# # print("Player two best resp strategy:")
# # trainer.playerTwoTree.PrintBestResp()
# # print("Player two regrets:")
# # trainer.playerTwoTree.PrintRegrets()
# #
# #
# # print("done")
#
#
# if (trainer.kuhn.IsPlayerOneCloseToNash(trainer.playerOneTree)):
#     print("Player one is in Nash")
# else:
#     print("Player one is not in Nash")
#
# if(trainer.kuhn.IsPlayerTwoCloseToNash(trainer.playerTwoTree)):
#     print("Player two is in Nash")
# else:
#     print("Player two is not in Nash")
#
#
# print("done")
#
#
