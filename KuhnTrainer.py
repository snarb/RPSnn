import tensorflow as tf
import numpy
import GameProcessor
import random
rng = numpy.random
import numpy as np
import math
import copy
from sklearn.preprocessing import normalize
from KuhnPoker import KuhnPoker, Players, Moves, Results, NextPlayer, MovesToOneHot, CardsToOneHot
#numpy.random.seed(12)

def Normalise(v):
    norm=np.linalg.norm(v, ord=1)
    if norm==0:
        norm=np.finfo(v.dtype).eps
    return v/norm

def MakeChoise(dist, batchSize):
    dist = Normalise(dist)
    return np.random.choice(len(dist), batchSize, p=dist)

# Parameters
learning_rate = 1e-4
training_epochs = 2000
SAMPLE_SIZE = 80
DISPLAY_STATS_STEP = 10

INPUT_SIZE = 4 # Max - three possible moves
OUTPUT_SIZE = 2 # Two actions: pass, bet

alpha = 0.1
beta = 0.005

# Network Parameters
n_hidden_1 = 54 # 1st layer number of features
n_hidden_2 = 54 # 2nd layer number of features
# # Store layers weight & bias
# weights = {
#     'h1': tf.Variable(tf.random_normal([INPUT_SIZE, n_hidden_1])),
#     'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
#     'out': tf.Variable(tf.random_normal([n_hidden_2, OUTPUT_SIZE]))
# }
# biases = {
#     'b1': tf.Variable(tf.random_normal([n_hidden_1])),
#     'b2': tf.Variable(tf.random_normal([n_hidden_2])),
#     'out': tf.Variable(tf.random_normal([OUTPUT_SIZE]))
# }

# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.ones([INPUT_SIZE, n_hidden_1])),
    'h2': tf.Variable(tf.ones([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.ones([n_hidden_2, OUTPUT_SIZE]))
}
biases = {
    'b1': tf.Variable(tf.ones([n_hidden_1])),
    'b2': tf.Variable(tf.ones([n_hidden_2])),
    'out': tf.Variable(tf.ones([OUTPUT_SIZE]))
}

infoState = tf.placeholder("float", [1, INPUT_SIZE], name= "infoState")

# Create model
def multilayer_perceptron(x, weights, biases):
    # Hidden layer with RELU activation
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)

    #dropOp1 = tf.nn.dropout(layer_1, 0.5)
    # Hidden layer with RELU activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)

    #dropOp2 = tf.nn.dropout(layer_2, 0.5)

    # Output layer with linear activation
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer


def TrainModel():

    # Construct model
    pred = tf.nn.softmax(multilayer_perceptron(infoState, weights, biases))
    Y = tf.placeholder(tf.float32, [1, OUTPUT_SIZE], name= "Y_output")

    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels = Y, logits = pred)
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)
    init = tf.global_variables_initializer()

    pokerEngine = KuhnPoker()
    permProb = 1.0 / len(pokerEngine.cardsPermutations)

    with tf.Session() as sess:
        sess.run(init)

        displayCyclePayoff = 0
        globalPayoff = 0
        roundsCount = 0
        lastPayoffCount = pokerEngine.PayoffCount

        for epoch in range(training_epochs):
            currentPayoff = UpdateSubGraphAndGetValue(sess, pred, optimizer, Y, pokerEngine, Players.one, permProb)
            displayCyclePayoff += currentPayoff
            if(pokerEngine.NewRound() == 1):
                roundsCount += 1
                if(roundsCount == DISPLAY_STATS_STEP):
                    roundsCount = 0
                    globalPayoff += displayCyclePayoff
                    gamesCount =  pokerEngine.PayoffCount - lastPayoffCount
                    p1Payoff = displayCyclePayoff
                    p2Payoff = -p1Payoff

                    strToPrint = "Cycle payoff. p1: {0:+.3f}, p2: {1:+.3f}" .format(p1Payoff / gamesCount, p2Payoff / gamesCount)
                    print(strToPrint)
                    lastPayoffCount = pokerEngine.PayoffCount
                    displayCyclePayoff = 0

        print("Total global payoff: ", globalPayoff)


def GetStateArray(pokerEngine, player):
    if (player == Players.one):
        card = pokerEngine.cards[0]
    else:
        card = pokerEngine.cards[1]

    carOneHot = CardsToOneHot[card]
    mixedAr = np.append(pokerEngine.infoSet, carOneHot)
    mixedAr = mixedAr.reshape((-1, len(mixedAr)))
    return mixedAr

def UpdateSubGraphAndGetValue(sess, pred, optimizer, Y, pokerEngine, player, graphProb):
    infosetBackup = pokerEngine.infoSet.copy()
    pokerEngineMoveId = pokerEngine.currentMoveId


    if (random.random() < beta):
        movesProbabileties = np.array([0.33, 0.33])
    else:
        mixedAr = GetStateArray(pokerEngine, player)
        movesProbabileties = sess.run(pred, feed_dict={infoState: mixedAr})[0]

    sampleSize = SAMPLE_SIZE * graphProb
    if(sampleSize < 1):
        if(random.random() < sampleSize):
            moveIds = MakeChoise(movesProbabileties, 1)
        else:
            moveIds = np.array([])
    else:
        sampleSize = round(sampleSize)
        moveIds = MakeChoise(movesProbabileties, sampleSize)

    totalPayoff = 0
    for moveId in moveIds:
        oneHotMove = MovesToOneHot[moveId + 1]
        pokerEngine.MakeOneHotMove(oneHotMove)
        if(pokerEngine.IsTerminateState()):
            currentPayoff = pokerEngine.GetPayoff(player)
        else:
            subGraphProb = graphProb * movesProbabileties[moveId]
            currentPayoff = -UpdateSubGraphAndGetValue(sess, pred, optimizer, Y, pokerEngine, NextPlayer(player), subGraphProb)

        totalPayoff += currentPayoff

        newMoveProb = movesProbabileties[moveId] + movesProbabileties[moveId] * currentPayoff * alpha
        movesProbabileties[moveId] = newMoveProb
        movesProbabileties = Normalise(movesProbabileties)

        pokerEngine.infoSet = infosetBackup.copy()
        pokerEngine.currentMoveId = pokerEngineMoveId

    Yar = movesProbabileties.reshape((-1, len(movesProbabileties)))
    mixedAr = GetStateArray(pokerEngine, player)
    sess.run(optimizer, feed_dict={Y: Yar, infoState: mixedAr})
    return totalPayoff


def GetSubSamplingPayOff(pokerEngine, player):
    infosetBackup = pokerEngine.infoSet.copy()
    pokerEngineMoveId = pokerEngine.currentMoveId

    movesProbabileties = [0.33, 0.33]
    moveIds = MakeChoise(movesProbabileties, SAMPLE_SIZE)

    totalPayoff = 0
    for moveId in moveIds:
        oneHotMove = MovesToOneHot[moveId + 1]
        pokerEngine.MakeOneHotMove(oneHotMove)
        if(pokerEngine.IsTerminateState()):
            totalPayoff += pokerEngine.GetPayoff(player)
        else:
            totalPayoff -= GetSubSamplingPayOff(pokerEngine, NextPlayer(player))

        pokerEngine.infoSet = infosetBackup.copy()
        pokerEngine.currentMoveId = pokerEngineMoveId

    return totalPayoff

def GetSingeRandomWalkPayoff(pokerEngine):
    if (bool(random.getrandbits(1))):
        pokerEngine.MakeMove(Moves.bet)
    else:
        pokerEngine.MakeMove(Moves.pas)

    if (pokerEngine.IsTerminateState()):
        return pokerEngine.GetPayoff(Players.one)
    else:
        return GetSingeRandomWalkPayoff(pokerEngine)




if __name__ == '__main__':
    TrainModel()
    # pokerEngine = KuhnPoker()
    # # totalPayoff = 0
    # #
    # # for _ in range(2000):
    # #     totalPayoff += RndGame(pokerEngine)
    # #     pokerEngine.NewRound()
    #
    # totalPayoff = 0
    # for _ in range(1000):
    #     currentPayoff = GetSubSamplingPayOff(pokerEngine, Players.one)
    #     totalPayoff += currentPayoff
    #     #print(pokerEngine.cards, currentPayoff)
    #     pokerEngine.NewRound()
    #
    # print("Total: ", totalPayoff)




