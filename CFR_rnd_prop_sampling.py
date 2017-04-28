import random
import Utils
from KuhnPoker import *
from treelib import Node, Tree
from CfrNode import CfrNode
from GameTree import GameTree
from matplotlib import pyplot as plt

class CFRtrainer:
    BETA = 0.00
    SAMPLE_SIZE = 5

    def __init__(self):
        self.playerOneTree = GameTree(CfrNode)
        self.playerTwoTree = GameTree(CfrNode)
        self.kuhn = KuhnPoker()

    # def UpdateUtil(self, curPlayer, util, strategy, action, p0, p1, isP1Freeze):
    #     if (curPlayer == Players.one):
    #         util[action] = -self.CFR(p0 * strategy[action], p1, isP1Freeze)
    #     else:
    #         util[action] = -self.CFR(p0, p1 * strategy[action], isP1Freeze)

    def CFR(self, p0, p1, isCurPlayerFreez):
        curPlayer = self.kuhn.GetCurrentPlayer()

        if(self.kuhn.IsTerminateState()):
            return self.kuhn.GetPayoff(curPlayer)

        curPlayerProb = p0 if curPlayer == Players.one else p1
        tree = self.playerOneTree if curPlayer == Players.one else self.playerTwoTree
        cfrNode = tree.GetOrCreateDataNode(self.kuhn, curPlayer)
        util = [0.0] * NUM_ACTIONS
        nodeUtil = 0

        if (random.random() < CFRtrainer.BETA):
            strategy = np.array([0.5] * NUM_ACTIONS)
        else:
            strategy = cfrNode.GetStrategy(curPlayerProb)

        #CFRtrainer.BETA *= 0.9

        sampleSize = max(int(round(CFRtrainer.SAMPLE_SIZE)), 1)
        actions = Utils.MakeChoise(strategy, sampleSize)


        infosetStr = self.kuhn.GetInfoset(curPlayer)

        repsCount = [0] * NUM_ACTIONS
        for action in actions:
            infosetBackup = self.kuhn.SaveInfoSet()
            self.kuhn.MakeAction(action)
            #self.UpdateUtil(curPlayer, util, strategy, action, p0, p1, isP1Freeze)
            if (curPlayer == Players.one):
                util[action] = -self.CFR(p0 * strategy[action], p1, not isCurPlayerFreez)
            else:
                util[action] = -self.CFR(p0, p1 * strategy[action], not isCurPlayerFreez)

            repsCount[action] += 1

            self.kuhn.RestoreInfoSet(infosetBackup)

        for action in range(NUM_ACTIONS):
            if(repsCount[action] > 0):
                util[action] /= repsCount[action]
                nodeUtil += strategy[action] * util[action]

        opProb = p1 if curPlayer == Players.one else p0
        if (isCurPlayerFreez):
            for action in range(NUM_ACTIONS):
                regret = util[action] - nodeUtil
                cfrNode.nextRegretSum[action] += opProb * regret
        else:
            for action in range(NUM_ACTIONS):
                regret = util[action] - nodeUtil
                cfrNode.regretSum[action] += opProb * regret
                cfrNode.regretSum[action] += cfrNode.nextRegretSum[action]
                cfrNode.nextRegretSum[action] = 0

        return nodeUtil

    def Train(self):
        util = 0
        cnt = 0

        results = []

        for i in range(1, 1000):
            self.kuhn.NewRound()
            util += self.CFR(1, 1)
            if(cnt % 100 == 0):
                results.append(util / i)

        print("Avg util:", util / i)
        plt.plot(results)
        plt.show()




trainer = CFRtrainer()
trainer.Train()

print("Player one avg strategy:")
trainer.playerOneTree.PrintAvgStrategy()
print("Player one best resp strategy:")
trainer.playerOneTree.PrintBestResp()
print("Player one regrets:")
trainer.playerOneTree.PrintRegrets()


print("----------------------")
print("Player two avg strategy:")
trainer.playerTwoTree.PrintAvgStrategy()
print("Player two best resp strategy:")
trainer.playerTwoTree.PrintBestResp()
print("Player two regrets:")
trainer.playerTwoTree.PrintRegrets()


print("done")

