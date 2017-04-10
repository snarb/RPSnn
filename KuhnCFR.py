from KuhnPoker import *
from treelib import Node, Tree
import numpy as np

class CfrNode:
    def __init__(self):
        self.regretSum = [0.0] * NUM_ACTIONS
        self.strategy = [0.0] * NUM_ACTIONS
        self.strategySum = [0.0] * NUM_ACTIONS

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

        return self.strategy


    def GetAverageStrategy(self):
        avgStrategy = [] * NUM_ACTIONS

        normalizingSum = 0
        for a in range(NUM_ACTIONS):
            normalizingSum += self.strategySum[a]

        for a in range(NUM_ACTIONS):
            if (normalizingSum > 0):
                avgStrategy[a] = self.strategySum[a] / normalizingSum
            else:
                avgStrategy[a] = 1.0 / NUM_ACTIONS
        return avgStrategy


class CFRtrainer:
    def __init__(self):
        self.playerOneTree = Tree()
        self.playerTwoTree = Tree()

        self.playerOneTree.create_node(identifier="root")
        self.playerTwoTree.create_node(identifier="root")

        self.playerOneLastNode = None
        self.playerTwoLastNode = None

        self.kuhn = KuhnPoker()

    def HasChild(self, parentId, childTag, tree):
        if(self.GetChildByTag(parentId, childTag, tree)):
            return True

        return False

    def GetChildByTag(self, parentId, childTag, tree):
        for childId in  tree.children(parentId):
            childNode = tree[childId]
            if(childNode.tag == childTag):
                return childNode

        return None

    def CFR(self, p0, p1):
        curPlayer = self.kuhn.GetCurrentPlayer()
        curPlayerProb = p0 if curPlayer == Players.one else p1
        tree = self.playerOneTree if curPlayer == Players.one else self.playerTwoTree

        if(self.kuhn.IsTerminateState()):
            return self.kuhn.GetPayoff(curPlayer)

        # lastMove = self.kuhn.infoSet[self.currentMoveId - 2]
        #
        # if(lastMove >= 0):

        # card = self.kuhn.GetPlayerCard(curPlayer)
        #
        # infoset = str(card) + " | " + str(self.kuhn.infoSet)
        #
        # if(previousInfoset not in tree):
        #     previousInfoset = 'root'
        lastNodeId = self.playerOneLastNode if curPlayer == Players.one else self.playerTwoLastNode
        lastMoveId = self.kuhn.currentMoveId - 1

        if(lastMoveId < 0):
            nodeId = lastNodeId
        else:
            lastMove = self.kuhn.infoSet[lastMoveId]

            if(self.HasChild(lastNodeId, lastMove, tree)):
                nodeId = self.GetChildByTag(lastNodeId, lastMove, tree).identifier
            else:
                nodeId = tree.create_node(tag=lastMove, data=CfrNode(), parent=lastNodeId).identifier

            if(curPlayer == Players.one):
                self.playerOneLastNode = nodeId
            else:
                self.playerTwoLastNode = nodeId

        node = tree[nodeId].data
        strategy = node.GetStrategy(curPlayerProb)
        util = [0.0] * NUM_ACTIONS
        nodeUtil = 0

        for a in range(NUM_ACTIONS):

            infosetBackup = self.kuhn.SaveInfoSet()

            self.kuhn.MakeMove(Moves(MovesToOneHot[a + 1]))
            if(curPlayer == Players.one):
                util[a] = -self.CFR(p0 * strategy[a], p1)
            else:
                util[a] = -self.CFR(p0, p1 * strategy[a])

            nodeUtil += strategy[a] * util[a]

            self.kuhn.RestoreInfoSet(infosetBackup)


        for a in range(NUM_ACTIONS):
            regret = util[a] - nodeUtil
            opProb = p1 if curPlayer == Players.one else p0
            node.regretSum[a] += opProb * regret

        return nodeUtil

    def Train(self):
        while (self.kuhn.NewRound() != 1):
            self.playerOneLastNode = self.playerOneTree.create_node(tag=self.kuhn.cards[0], data = CfrNode(), parent='root').identifier
            self.playerTwoLastNode = self.playerTwoTree.create_node(tag=self.kuhn.cards[1], parent='root').identifier

            self.CFR(1, 1)


trainer = CFRtrainer()
for i in range(100):
    trainer.Train()

print("done")

