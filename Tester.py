from KuhnPoker import *
import Utils
from matplotlib import pyplot as plt
from m3 import CFRtrainer as  rndSampler
from KuhnCFR import CFRtrainer as vanillaCFR

def CFR(kuhn, playerOneTree, playerTwoTree):
    curPlayer = kuhn.GetCurrentPlayer()

    if (kuhn.IsTerminateState()):
        return kuhn.GetPayoff(curPlayer)

    tree = playerOneTree if curPlayer == Players.one else playerTwoTree
    cfrNode = tree.GetOrCreateDataNode(kuhn, curPlayer)
    strategy = cfrNode.GetAverageStrategy()

    action = Utils.MakeChoise(strategy, 1)[0]
    kuhn.MakeAction(action)
    util = CFR(kuhn, playerOneTree, playerTwoTree)
    return util


def Test(playerOneTree, playerTwoTree):
        kuhn = KuhnPoker()
        util = 0

        for i in range(1, 5000):
            kuhn.NewRound()
            util += CFR(kuhn, playerOneTree, playerTwoTree)

        return util / i



print("Training vanillaCFR")
vanillaCFRtrainer = vanillaCFR()
vanillaCFRtrainer.Train()

util2 = Test(vanillaCFRtrainer.playerOneTree, vanillaCFRtrainer.playerTwoTree)

# print("Training rndSampler")
# rndTrainer = rndSampler()
# rndTrainer.Train()
#
# util1 = Test(vanillaCFRtrainer.playerOneTree, rndTrainer.playerTwoTree)
# print("Avg util vanillaCFR (p1) vs rndSampler (p2):", util1)

#util2 = Test(rndTrainer.playerOneTree, vanillaCFRtrainer.playerTwoTree)
print("Avg util rndSampler (p1) vs rndSampler (p2):", util2)