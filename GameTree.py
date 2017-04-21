from treelib import Node, Tree
# from StateNode import StateNode
from CfrNode import CfrNode
from copy import deepcopy
import numpy as np

class GameTree:
    def __init__(self):
        self.tree = Tree()
        self.tree.create_node(identifier="GameTree")

    # def _addNode(self, nodeName, data, parent):
    #     if(parent):
    #         createdNode = self.tree.create_node(tag=nodeName, data=data, parent=parent)
    #     else:
    #         createdNode = self.tree.create_node(tag=nodeName, data=data, parent="root")
    #
    #     return createdNode


    # def GetOrCreateStateNode(self, infostate):
    #     if (infostate in self.tree):
    #         return self.tree[infostate].data
    #
    #     # return self._addNode(stateName, StateNode(stateName), parent=parent)
    #     return self.tree.create_node(identifier=infostate, data=StateNode(infostate), parent="root").data

    def GetOrCreateCFRNode(self, kuhnEngine, curPlayer):
        infoset = kuhnEngine.GetInfoset(curPlayer)

        if (infoset in self.tree):
            return self.tree[infoset].data

        tag = kuhnEngine.GetPrettyLastMove(curPlayer)
        prevInfoset = kuhnEngine.GetPrevInfoset(curPlayer)

        if (prevInfoset not in self.tree):
            prevTag = str(kuhnEngine.GetPlayerCard(curPlayer))
            return self.tree.create_node(identifier=prevInfoset, tag=prevTag, data=CfrNode(infoset), parent="GameTree").data

        if (infoset != prevInfoset):
            return self.tree.create_node(identifier=infoset, tag=tag, data=CfrNode(infoset), parent=prevInfoset).data


    def __getitem__(self, key):
        return self.tree[key]

    def __contains__(self, key):
        return key in self.tree


    def _printFunc(self, func):
        #float_formatter = lambda x: "%.2f" % x

        treeCopy = deepcopy(self.tree)

        for nodeId in treeCopy.expand_tree():
            node = treeCopy[nodeId]
            gameNode = node.data
            if(gameNode):
                node.tag += " " + str(func(gameNode))

        print(treeCopy.show())


    def PrintAvgStrategy(self):
        self._printFunc(lambda gameNode: gameNode.GetAverageStrategy())

    def PrintBestResp(self):
        self._printFunc(lambda gameNode: gameNode.GetStrategy(1.0))

    def PrintRegrets(self):
        self._printFunc(lambda gameNode: gameNode.regretSum)

    def PrintStrategy(self):
        self._printFunc(lambda gameNode: gameNode.strategy)







