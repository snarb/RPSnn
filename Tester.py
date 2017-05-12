from KuhnPoker import *
import Utils
#from matplotlib import pyplot as plt
#from m3 import CFRtrainer as  rndSampler
from KuhnCFR import CFRtrainer as vanillaCFR
#from rnd_smapling_2 import RndSampler

#from severalMove import CFRtrainer as RndSampler


def CFR(kuhn, playerOneTree, playerTwoTree):
    curPlayer = kuhn.GetCurrentPlayer()

    if (kuhn.IsTerminateState()):
        return kuhn.GetPayoff(curPlayer)

    tree = playerOneTree if curPlayer == Players.one else playerTwoTree
    cfrNode = tree.GetOrCreateDataNode(kuhn, curPlayer)
    strategy = cfrNode.GetAverageStrategy()

    action = Utils.MakeChoise(strategy, 1)[0]
    kuhn.MakeAction(action)
    util = -CFR(kuhn, playerOneTree, playerTwoTree)
    return util


def Test(playerOneTree, playerTwoTree):
        kuhn = KuhnPoker()
        util = 0

        for i in range(1, 8000):
            kuhn.NewRound()
            curUtil = CFR(kuhn, playerOneTree, playerTwoTree)
            util += curUtil

        return util / i



print("Training vanillaCFR")

sumU = 0
countU = 0

for i in range(10):
    vanillaCFRtrainer1 = vanillaCFR(1.0)
    vanillaCFRtrainer1.Train()

    vanillaCFRtrainer2 = vanillaCFR(10)
    vanillaCFRtrainer2.Train()

    # vanillaCFRtrainer.CheckNash()
    testUtil1 = Test(vanillaCFRtrainer1.playerOneTree, vanillaCFRtrainer2.playerTwoTree)
    #print("Vanilla safe play test util: ", testUtil1)


    testUtil2 = Test(vanillaCFRtrainer2.playerOneTree, vanillaCFRtrainer1.playerTwoTree)
    sumU += testUtil1 + (-testUtil2)
    countU += 1


print("Avg Vanila profit 1: ", sumU / countU)
print(countU)
    #print("Vanilla safe play test util: _2", testUtil2)



#print("Vanila profit 1 ", testUtil1 + (-testUtil2))

# print("Training rndSampler")
# rndTrainer = RndSampler()
# rndTrainer.Train()
#
# vanila1 = Test(vanillaCFRtrainer.playerOneTree, rndTrainer.playerTwoTree)
# print("Avg util vanillaCFR (p1) vs rndSampler (p2):", vanila1)
#
# vanila2 = Test(rndTrainer.playerOneTree, vanillaCFRtrainer.playerTwoTree)
# print("Avg util rndSampler (p1) vs vanillaCFR (p2):", vanila2)
#
#
# print("Vanila profit", vanila1 + (-vanila2))