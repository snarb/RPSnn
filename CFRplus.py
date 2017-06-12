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
    def __init__(self):
        self.playerOneTree = GameTree(CfrNode)
        self.playerTwoTree = GameTree(CfrNode)
        self.kuhn = KuhnPoker()
        self.stats = Counter()
        #self.alpha = alpha
        self.trainigXdata = []
        self.trainigYdata = []
        self.hists = []
        self.avgStr = []
        self.stratSum = 0
        self.iter = 0
        self.betRegrets = []

    def CFR(self, p0, p1):
        curPlayer = self.kuhn.GetCurrentPlayer()

        if(self.kuhn.IsTerminateState()):
            return self.kuhn.GetPayoff(curPlayer)

        curPlayerProb = p0 if curPlayer == Players.one else p1
        opProb = p1 if curPlayer == Players.one else p0

        tree = self.playerOneTree if curPlayer == Players.one else self.playerTwoTree
        cfrNode = tree.GetOrCreateDataNode(self.kuhn, curPlayer)
        strategy = cfrNode.GetStrategy(curPlayerProb)

        util = [0.0] * NUM_ACTIONS
        nodeUtil = 0

        infosetStr = self.kuhn.GetInfoset(curPlayer)

        infosetBackup = self.kuhn.SaveInfoSet()


        for action in range(NUM_ACTIONS):
            self.kuhn.MakeAction(action)

            if(curPlayer == Players.one):
                util[action] += -self.CFR(p0 * strategy[action], p1)
            else:
                util[action] += -self.CFR(p0, p1 * strategy[action])

            nodeUtil += strategy[action] * util[action]
            self.kuhn.RestoreInfoSet(infosetBackup)

        for action in range(NUM_ACTIONS):
            regret = util[action]  - nodeUtil
            cfrNode.regretSum[action] = cfrNode.regretSum[action]  +  opProb * regret


        if(('1 | uplayed;uplayed;uplayed' in infosetStr) and curPlayer == Players.one):
            self.trainigXdata.append(np.array(strategy))
            self.trainigYdata.append(nodeUtil)

            self.betRegrets.append(cfrNode.regretSum[1])

            self.stratSum += strategy[1]
            self.avgStr.append(self.stratSum / (len(self.avgStr) + 1))

            self.iter += 1

        return nodeUtil

    def running_mean(self, x, N):
        cumsum = np.cumsum(np.insert(x, 0, 0))
        return (cumsum[N:] - cumsum[:-N]) / N

    def Train(self):
        util = 0
        cnt = 0
        start_time = time.time()

        results = []
        # utils = []
        for i in range(1, 500):
            self.kuhn.NewRound()
            curUtil = self.CFR(1, 1)
            util += curUtil
            if(cnt % 80 == 0):
                results.append(util / i)



    def CheckNash(self):
        if (self.kuhn.IsPlayerOneCloseToNash(self.playerOneTree)):
            print("Player one is in Nash")
        else:
            print("Player one is not in Nash")

        if(self.kuhn.IsPlayerTwoCloseToNash(self.playerTwoTree)):
            print("Player two is in Nash")
        else:
            print("Player two is not in Nash")


