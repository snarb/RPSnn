from KuhnPoker import *
from treelib import Node, Tree
from CfrNode import CfrNode
from GameTree import GameTree
from matplotlib import pyplot as plt
import Utils
import math

class CFRtrainer:
    def __init__(self):
        self.playerOneTree = GameTree(CfrNode)
        self.playerTwoTree = GameTree(CfrNode)
        self.kuhn = KuhnPoker()

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
        tree = self.playerOneTree if curPlayer == Players.one else self.playerTwoTree
        cfrNode = tree.GetOrCreateDataNode(self.kuhn, curPlayer)
        strategy = cfrNode.GetStrategy(curPlayerProb)
        util = [0.0] * NUM_ACTIONS
        nodeUtil = 0

        infosetStr = self.kuhn.GetInfoset(curPlayer)
        infosetBackup = self.kuhn.SaveInfoSet()

        #'1 | bet;bet;uplayed'
        #'1 | bet;pas;uplayed'

        # if(('1 | bet;bet' in infosetStr) and curPlayer == Players.one):
        #     g = 6

        for action in range(NUM_ACTIONS):
            self.kuhn.MakeAction(action)

            if(curPlayer == Players.one):
                util[action] = -self.CFR(p0 * strategy[action], p1)
            else:
                util[action] = -self.CFR(p0, p1 * strategy[action])

            cfrNode.util[action] += util[action]

            nodeUtil += strategy[action] * util[action]

            self.kuhn.RestoreInfoSet(infosetBackup)

        for action in range(NUM_ACTIONS):
            regret = util[action]  - nodeUtil
            opProb = p1 if curPlayer == Players.one else p0
            cfrNode.regretSum[action] += opProb * regret



#0445733333
        return nodeUtil

    def running_mean(self, x, N):
        cumsum = np.cumsum(np.insert(x, 0, 0))
        return (cumsum[N:] - cumsum[:-N]) / N

    def Train(self):
        util = 0
        cnt = 0

        # self.playerOneTree.GetOrCreateCFRNode(self.kuhn, Players.one)
        # self.playerTwoTree.GetOrCreateCFRNode(self.kuhn, Players.one)

        # while (self.kuhn.NewRound() != 1):
        #     util += self.CFR(1, 1)
        #     cnt += 1
        #     if(cnt % 10 == 0):
        #         print(util / cnt)
        results = []
        # utils = []
        for i in range(1, 10000):
            self.kuhn.NewRound()
            curUtil = self.CFR(1, 1)
            # utils.append(curUtil)
            util += curUtil
            if(cnt % 100 == 0):
                results.append(util / i)

        print("Avg util:", util / i)
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





trainer = CFRtrainer()
trainer.Train()
#
print("Player one avg strategy:")
trainer.playerOneTree.PrintAvgStrategy()
print("Player one best resp strategy:")
trainer.playerOneTree.PrintBestResp()

print("Player Util regret strategy:")
trainer.playerOneTree.PrintUtilRegretStrategy()

print("Player Util strategy:")
trainer.playerOneTree.GetUtilStrategy()

print("Player Utils:")
trainer.playerOneTree.PrintUtils()


print("Player one regrets:")
trainer.playerOneTree.PrintRegrets()
#
#
# print("----------------------")
# print("Player two avg strategy:")
# trainer.playerTwoTree.PrintAvgStrategy()
# # print("Player two best resp strategy:")
# # trainer.playerTwoTree.PrintBestResp()
# # print("Player two regrets:")
# # trainer.playerTwoTree.PrintRegrets()
#

#
# print("Max dif: " , KuhnPoker.MaxDif)
# print("done")
#
