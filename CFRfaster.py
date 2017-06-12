from KuhnPoker import *
from treelib import Node, Tree
from CfrNode import CfrNode
from GameTree import GameTree
from matplotlib import pyplot as plt
import Utils
import math
from collections import Counter
from math import sqrt
import random
import time
import pandas as pd

from NodeEstimator import Estimator

class CFRtrainer:
    def __init__(self, alpha):
        self.playerOneTree = GameTree(CfrNode)
        self.playerTwoTree = GameTree(CfrNode)
        self.kuhn = KuhnPoker()
        self.stats = Counter()
        self.alpha = alpha
        self.trainigXdata = []
        self.trainigYdata = []
        self.hists = []
        self.avgStr = []
        self.stratSum = 0
        self.iter = 0
        self.betRegrets = []


    # def HasChild(self, parentId, childTag, tree):
    #     if(self.GetChildByTag(parentId, childTag, tree)):
    #         return True
    #
    #     return False
    #
    # def GetChildByTag(self, parentId, childTag, tree):
    #     for childId in  tree.children(parentId):
    #         childNode = tree[childId]
    #         if(childNode.tag == childTag):
    #             return childNode
    #
    #     return None

    def CFR(self, p0, p1):
        curPlayer = self.kuhn.GetCurrentPlayer()

        if(self.kuhn.IsTerminateState()):
            return self.kuhn.GetPayoff(curPlayer)

        curPlayerProb = p0 if curPlayer == Players.one else p1
        opProb = p1 if curPlayer == Players.one else p0

        tree = self.playerOneTree if curPlayer == Players.one else self.playerTwoTree
        cfrNode = tree.GetOrCreateDataNode(self.kuhn, curPlayer)
        strategy = cfrNode.GetStrategy(curPlayerProb)

        # if(random.random() < 0.9):
        #     strategy = cfrNode.GetStrategy(curPlayerProb)
        # else:
        #     strategy = cfrNode.GetAverageStrategy()

        util = [0.0] * NUM_ACTIONS
        nodeUtil = 0

        infosetStr = self.kuhn.GetInfoset(curPlayer)


        # if(infosetStr == '2 | pas;bet;uplayed'):
        #     card = self.kuhn.GetPlayerCard(Players.two)
        #     self.stats[card] += card * opProb

        infosetBackup = self.kuhn.SaveInfoSet()

        #'1 | bet;bet;uplayed'
        #'1 | bet;pas;uplayed'


            # g = 6

        # if (('1 | bet;bet' in infosetStr) and curPlayer == Players.one):
        #     g = 6

        for action in range(NUM_ACTIONS):
            self.kuhn.MakeAction(action)

            if(curPlayer == Players.one):
                util[action] += -self.CFR(p0 * strategy[action], p1)
                #util[action] += -self.CFR(p0 * strategy[action], p1)
            else:
                util[action] += -self.CFR(p0, p1 * strategy[action])
                #util[action] += -self.CFR(p0, p1 * strategy[action])

            #util[action] /= 2

            nodeUtil += strategy[action] * util[action]

            self.kuhn.RestoreInfoSet(infosetBackup)

        for action in range(NUM_ACTIONS):
            regret = util[action]  - nodeUtil
            # if(regret > 0):
            #     regret = regret
            # else:
            #     regret = 0

            #regret = max(0, regret)
            cfrNode.regretSum[action] = cfrNode.regretSum[action]  +  opProb * regret


        if(('1 | uplayed;uplayed;uplayed' in infosetStr) and curPlayer == Players.one):
            self.trainigXdata.append(np.array(strategy))
            self.trainigYdata.append(nodeUtil)

            self.betRegrets.append(cfrNode.regretSum[1])

            self.stratSum += strategy[1]
            self.avgStr.append(self.stratSum / (len(self.avgStr) + 1))

            # if(self.iter % 300 == 0):
            #     xa = np.array(self.trainigXdata)[:, 1]
            #     bins = np.linspace(0, 1, num=5)
            #     hist, bin_edges = np.histogram(xa, bins=bins, density=False)
            #     self.hists.append((hist, bin_edges))
            #     self.trainigXdata.clear()
            #     self.trainigYdata.clear()

            self.iter += 1


            if (strategy[0] != 1):
                strategy = strategy
#0445733333
        return nodeUtil

    def running_mean(self, x, N):
        cumsum = np.cumsum(np.insert(x, 0, 0))
        return (cumsum[N:] - cumsum[:-N]) / N

    def Train(self):
        util = 0
        cnt = 0
        start_time = time.time()

        # self.playerOneTree.GetOrCreateCFRNode(self.kuhn, Players.one)
        # self.playerTwoTree.GetOrCreateCFRNode(self.kuhn, Players.one)

        # while (self.kuhn.NewRound() != 1):
        #     util += self.CFR(1, 1)
        #     cnt += 1
        #     if(cnt % 10 == 0):
        #         print(util / cnt)


        results = []
        # utils = []
        for i in range(1, 3000):
            self.kuhn.NewRound()
            curUtil = self.CFR(1, 1)
            # utils.append(curUtil)
            util += curUtil
            if(cnt % 80 == 0):
                results.append(util / i)


        # plt.plot(self.avgStr)
        # plt.show()
        #
        # res = pd.rolling_mean(self.avgStr, window = 2)
        # plt.plot(res)
        # plt.show()

        # plt.plot(self.betRegrets)
        # plt.axhline(0, color='r')
        # plt.show()


        # plt.ion()
        # for i in range(len(self.hists)):
        #     hist, bins = self.hists[i]
        #     width = 0.7 * (bins[1] - bins[0])
        #     center = (bins[:-1] + bins[1:]) / 2
        #
        #     self.betRegrets()
        #     plt.bar(center, hist, align='center', width=width)
        #     plt.pause(2)
        #     plt.clf()
        #
        # while True:
        #     plt.pause(0.05)
        #
        # estimator = Estimator()
        # realX, predX = estimator.Train(self.trainigXdata, self.trainigYdata)
        #
        #
        #
        #
        # plt.plot(np.array(self.trainigXdata)[:, 1][100:], self.trainigYdata[100:])
        # plt.show()
        #
        # xa = np.array(self.trainigXdata[3000:])[:, 1]
        # ya = self.trainigYdata[3000:]
        #
        #
        #
        #
        # heatmap, xedges, yedges = np.histogram2d(xa, ya, bins=10)
        # extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        #
        # plt.clf()
        # plt.imshow(heatmap.T, extent=extent, origin='lower')
        # plt.show()
        #
        #
        #
        # missCount = 50
        # t = range(len(xa) - missCount)
        # plt.scatter(xa[missCount:], ya[missCount:], c=t)
        # plt.show()
        # plt.plot(xa[missCount:], ya[missCount:])
        # plt.plot(realX, predX)
        # plt.show()

        # print("Time: ", time.time() - start_time)
        # print("Avg util:", util / i)
        # plt.plot(results)
        # plt.show()

    def CheckNash(self):
        if (self.kuhn.IsPlayerOneCloseToNash(self.playerOneTree)):
            print("Player one is in Nash")
        else:
            print("Player one is not in Nash")

        if(self.kuhn.IsPlayerTwoCloseToNash(self.playerTwoTree)):
            print("Player two is in Nash")
        else:
            print("Player two is not in Nash")





trainer = CFRtrainer(1)
trainer.Train()
trainer.CheckNash()
print("Player one avg strategy:")
trainer.playerOneTree.PrintAvgStrategy()
print("Player one best resp strategy:")
trainer.playerOneTree.PrintBestResp()
#
# # # print("Player one regrets:")
# # # trainer.playerOneTree.PrintRegrets()
# #
# #
# print("----------------------")
# print("Player two avg strategy:")
# trainer.playerTwoTree.PrintAvgStrategy()
# print("Player two best resp strategy:")
# trainer.playerTwoTree.PrintBestResp()
# # print("Player two regrets:")
# # trainer.playerTwoTree.PrintRegrets()
#

#
# print("Max dif: " , KuhnPoker.MaxDif)
# print("done")
#

