from KuhnPoker import *
from treelib import Node, Tree
from CfrNode import CfrNode
from GameTree import GameTree

class CFRtrainer:
    def __init__(self):
        self.playerOneTree = GameTree()
        self.playerTwoTree = GameTree()
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


        # lastNodeId = self.playerOneLastNode if curPlayer == Players.one else self.playerTwoLastNode
        # lastMoveId = self.kuhn.currentMoveId - 1
        #
        # if(lastMoveId < 0):
        #     nodeId = lastNodeId
        # else:
        #     lastMove = self.kuhn.infoSet[lastMoveId]
        #
        #     if(self.HasChild(lastNodeId, lastMove, tree)):
        #         nodeId = self.GetChildByTag(lastNodeId, lastMove, tree).identifier
        #     else:
        #         nodeId = tree.create_node(tag=lastMove, data=CfrNode(), parent=lastNodeId).identifier
        #
        #     if(curPlayer == Players.one):
        #         self.playerOneLastNode = nodeId
        #     else:
        #         self.playerTwoLastNode = nodeId

        # infoset = self.kuhn.GetInfoset(curPlayer)
        #
        # if (infoset in tree):
        #     gameNode = tree[infoset]
        # else:
        #     gameNode = tree.AddCFRNode(infoset, self.kuhn, curPlayer)
            #node = tree.create_node(tag=lastMove, data=CfrNode(), parent=lastNodeId).identifier

        # cfrNode = gameNode.data

        cfrNode = tree.GetOrCreateCFRNode(self.kuhn, curPlayer)
        strategy = cfrNode.GetStrategy(curPlayerProb)
        util = [0.0] * NUM_ACTIONS
        nodeUtil = 0

        for a in range(NUM_ACTIONS):

            infosetBackup = self.kuhn.SaveInfoSet()

            curMove = Moves(MovesToOneHot[a + 1])
            self.kuhn.MakeMove(curMove)
            if(curPlayer == Players.one):
                util[a] = -self.CFR(p0 * strategy[a], p1)
            else:
                util[a] = -self.CFR(p0, p1 * strategy[a])

            nodeUtil += strategy[a] * util[a]

            self.kuhn.RestoreInfoSet(infosetBackup)


        for a in range(NUM_ACTIONS):
            regret = util[a] - nodeUtil
            opProb = p1 if curPlayer == Players.one else p0
            cfrNode.regretSum[a] += opProb * regret

        return nodeUtil

    def Train(self):
        while (self.kuhn.NewRound() != 1):
            self.playerOneTree.GetOrCreateCFRNode(self.kuhn, Players.one)
            self.playerTwoTree.GetOrCreateCFRNode(self.kuhn, Players.one)
            self.CFR(1, 1)


trainer = CFRtrainer()
for i in range(1000):
    trainer.Train()

print("Player one avg strategy:")
trainer.playerOneTree.PrintAvgStrategy()
print("Player one best resp strategy:")
trainer.playerOneTree.PrintBestResp()

print("----------------------")
print("Player two avg strategy:")
trainer.playerTwoTree.PrintAvgStrategy()
print("Player two best resp strategy:")
trainer.playerTwoTree.PrintBestResp()



print("done")

