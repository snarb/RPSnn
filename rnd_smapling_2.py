import random
import Utils
from KuhnPoker import *
from treelib import Node, Tree
from CfrNode import CfrNode
from GameTree import GameTree
from matplotlib import pyplot as plt

class RndSampler:
    BETA = 0.0
    SAMPLE_SIZE = 1

    def __init__(self):
        self.playerOneTree = GameTree(CfrNode)
        self.playerTwoTree = GameTree(CfrNode)
        self.kuhn = KuhnPoker()

    # def UpdateUtil(self, curPlayer, util, strategy, action, p0, p1, isP1Freeze):
    #     if (curPlayer == Players.one):
    #         util[action] = -self.CFR(p0 * strategy[action], p1, isP1Freeze)
    #     else:
    #         util[action] = -self.CFR(p0, p1 * strategy[action], isP1Freeze)

    def CFR(self, p0, p1):
        curPlayer = self.kuhn.GetCurrentPlayer()

        if(self.kuhn.IsTerminateState()):
            return self.kuhn.GetPayoff(curPlayer)

        curPlayerProb = p0 if curPlayer == Players.one else p1
        tree = self.playerOneTree if curPlayer == Players.one else self.playerTwoTree
        cfrNode = tree.GetOrCreateDataNode(self.kuhn, curPlayer)
        util = [0.0] * NUM_ACTIONS
        nodeUtil = 0

        strategy = cfrNode.GetStrategy(curPlayerProb)

        if (random.random() < RndSampler.BETA):
            sampleStrategy = np.array([0.5] * NUM_ACTIONS)
        else:
            sampleStrategy = strategy

        sampleStrategy = Utils.Normalise(sampleStrategy)

        sampleSize = max(int(round(RndSampler.SAMPLE_SIZE)), 1)
        actions = Utils.MakeChoise(sampleStrategy, sampleSize)


        infosetStr = self.kuhn.GetInfoset(curPlayer)


        repsCount = [0] * NUM_ACTIONS
        for action in actions:
            infosetBackup = self.kuhn.SaveInfoSet()
            self.kuhn.MakeAction(action)
            if (curPlayer == Players.one):
                util[action] += -self.CFR(p0 * strategy[action], p1)
            else:
                util[action] += -self.CFR(p0, p1 * strategy[action])

            repsCount[action] += 1

            self.kuhn.RestoreInfoSet(infosetBackup)

        for action in range(NUM_ACTIONS):
            if(repsCount[action] > 0):
                util[action] /= repsCount[action]
                nodeUtil += strategy[action] * util[action]

        opProb = p1 if curPlayer == Players.one else p0

        for action in range(NUM_ACTIONS):
            regret = util[action] - nodeUtil
            cfrNode.regretSum[action] += opProb * regret

        return nodeUtil

    def Train(self):
        util = 0
        cnt = 0

        results = []

        for i in range(1, 2000):
            self.kuhn.NewRound()
            util += self.CFR(1, 1)
            if(cnt % 100 == 0):
                results.append(util / i)

            # RndSampler.BETA *= 0.9999

        print("Avg util:", util / i)
        plt.plot(results)
        plt.show()
        print("Beta ", RndSampler.BETA)




trainer = RndSampler()
trainer.Train()

print("Player one avg strategy:")
trainer.playerOneTree.PrintAvgStrategy()
# print("Player one best resp strategy:")
# trainer.playerOneTree.PrintBestResp()
# print("Player one regrets:")
# trainer.playerOneTree.PrintRegrets()


print("----------------------")
print("Player two avg strategy:")
trainer.playerTwoTree.PrintAvgStrategy()
# print("Player two best resp strategy:")
# trainer.playerTwoTree.PrintBestResp()
# print("Player two regrets:")
# trainer.playerTwoTree.PrintRegrets()


if (trainer.kuhn.IsPlayerOneCloseToNash(trainer.playerOneTree)):
    print("Player one is in Nash")
else:
    print("Player one is not in Nash")

if(trainer.kuhn.IsPlayerTwoCloseToNash(trainer.playerTwoTree)):
    print("Player two is in Nash")
else:
    print("Player two is not in Nash")


print("done")

