from KuhnPoker import *
import Utils
#from matplotlib import pyplot as plt
#from m3 import CFRtrainer as  rndSampler
from KuhnCFR import CFRtrainer as vanillaCFR
#from rnd_smapling_2 import RndSampler

#from severalMove import CFRtrainer as RndSampler


def CFR(kuhn, playerOneTree, playerTwoTree, isP1mega = False, isP2mega = False):
    curPlayer = kuhn.GetCurrentPlayer()

    if (kuhn.IsTerminateState()):
        return kuhn.GetPayoff(curPlayer)

    tree = playerOneTree if curPlayer == Players.one else playerTwoTree
    cfrNode = tree.GetOrCreateDataNode(kuhn, curPlayer)

    if((curPlayer == Players.one and isP1mega) or (curPlayer == Players.two and isP2mega)):
        strategy = cfrNode.GetMegaAvgStrategy()
    else:
        strategy = cfrNode.GetAverageStrategy()

    action = Utils.MakeChoise(strategy, 1)[0]
    kuhn.MakeAction(action)
    util = -CFR(kuhn, playerOneTree, playerTwoTree, isP1mega, isP2mega)
    return util


def Test(playerOneTree, playerTwoTree, isP1mega = False, isP2mega = False):
        kuhn = KuhnPoker()
        util = 0

        for i in range(1, 8000):
            kuhn.NewRound()
            curUtil = CFR(kuhn, playerOneTree, playerTwoTree, isP1mega, isP2mega)
            util += curUtil

        return util / i



print("Training vanillaCFR")

sumU = 0
countU = 0

for i in range(5):
    vanillaCFRtrainer1 = vanillaCFR()
    vanillaCFRtrainer1.Train()

    vanillaCFRtrainer2 = vanillaCFR()
    vanillaCFRtrainer2.Train()

    # vanillaCFRtrainer.CheckNash()
    testUtil1 = Test(vanillaCFRtrainer1.playerOneTree, vanillaCFRtrainer2.playerTwoTree, isP1mega = True, isP2mega = False)
    #print("Vanilla safe play test util: ", testUtil1)


    testUtil2 = Test(vanillaCFRtrainer2.playerOneTree, vanillaCFRtrainer1.playerTwoTree, isP1mega = False, isP2mega = True)
    sumU += testUtil1 + (-testUtil2)
    countU += 1
    print("round", i)


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