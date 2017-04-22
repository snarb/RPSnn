from KuhnPoker import *
from treelib import Node, Tree
from CfrNode import CfrNode
from GameTree import GameTree
from matplotlib import pyplot as plt

class CFRtrainer:
    def __init__(self):
        self.playerOneTree = GameTree()
        self.playerTwoTree = GameTree()
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
        curPlayerProb = p0 if curPlayer == Players.one else p1
        tree = self.playerOneTree if curPlayer == Players.one else self.playerTwoTree

        if(self.kuhn.IsTerminateState()):
            return self.kuhn.GetPayoff(curPlayer)

        cfrNode = tree.GetOrCreateCFRNode(self.kuhn, curPlayer)
        strategy = cfrNode.GetStrategy(curPlayerProb)
        util = [0.0] * NUM_ACTIONS
        nodeUtil = 0

        infosetStr = self.kuhn.GetInfoset(curPlayer)

        for action in range(NUM_ACTIONS):
            infosetBackup = self.kuhn.SaveInfoSet()
            curMove = Moves(MovesToOneHot[action + 1])
            self.kuhn.MakeMove(curMove)

            if(curPlayer == Players.one):
                util[action] = -self.CFR(p0 * strategy[action], p1)
            else:
                util[action] = -self.CFR(p0, p1 * strategy[action])

            nodeUtil += strategy[action] * util[action]

            self.kuhn.RestoreInfoSet(infosetBackup)

        for action in range(NUM_ACTIONS):
            regret = util[action] - nodeUtil
            opProb = p1 if curPlayer == Players.one else p0
            cfrNode.regretSum[action] += opProb * regret

        return nodeUtil

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

        for i in range(1, 1000):
            self.kuhn.NewRound()
            util += self.CFR(1, 1)
            if(cnt % 100 == 0):
                results.append(util / i)


                # print(i, util / i)

        plt.plot(results)
        plt.show()


trainer = CFRtrainer()
for i in range(1):
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

