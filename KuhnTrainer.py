import tensorflow as tf
import numpy
import GameProcessor
import matplotlib.pyplot as plt
import random
rng = numpy.random
import numpy as np
import copy
from sklearn.preprocessing import normalize
from KuhnPoker import KuhnPoker, Players, Moves, Results, NextPlayer, MovesToOneHot
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
training_epochs = 1000
SAMPLE_SIZE = 5

INPUT_SIZE = 3 # Max - three possible moves
OUTPUT_SIZE = 2 # Two actions: pass, bet

alpha = 0.5
beta = 0.01

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
    # Hidden layer with RELU activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)
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

    with tf.Session() as sess:
        sess.run(init)

        totalPayoff = 0
        globalPayoff = 0
        for epoch in range(training_epochs):
            currentPayoff = UpdateSubGraphAndGetValue(sess, pred, optimizer, Y, pokerEngine, Players.one)
            totalPayoff += currentPayoff
            if(pokerEngine.NewRound() == 1):
                globalPayoff += totalPayoff
                print("Total cycle payoff: ", totalPayoff)
                totalPayoff = 0

        print("Total global payoff: ", globalPayoff)


def UpdateSubGraphAndGetValue(sess, pred, optimizer, Y, pokerEngine, player):
    infosetBackup = pokerEngine.infoSet.copy()
    pokerEngineMoveId = pokerEngine.currentMoveId


    if (random.random() < beta):
        movesProbabileties = [0.33, 0.33]
    else:
        infosetAr = pokerEngine.infoSet.reshape((-1, len(pokerEngine.infoSet)))
        movesProbabileties = sess.run(pred, feed_dict={infoState: infosetAr})[0]

    moveIds = MakeChoise(movesProbabileties, SAMPLE_SIZE)

    totalPayoff = 0
    for moveId in moveIds:
        oneHotMove = MovesToOneHot[moveId + 1]
        pokerEngine.MakeOneHotMove(oneHotMove)
        if(pokerEngine.IsTerminateState()):
            currentPayoff = pokerEngine.GetPayoff(player)
        else:
            currentPayoff = -UpdateSubGraphAndGetValue(sess, pred, optimizer, Y, pokerEngine, NextPlayer(player))

        totalPayoff += currentPayoff

        newMoveProb = movesProbabileties[moveId] + movesProbabileties[moveId] * currentPayoff * alpha
        movesProbabileties[moveId] = newMoveProb
        movesProbabileties = Normalise(movesProbabileties)

        pokerEngine.infoSet = infosetBackup.copy()
        pokerEngine.currentMoveId = pokerEngineMoveId

    Yar = movesProbabileties.reshape((-1, len(movesProbabileties)))
    infosetAr = pokerEngine.infoSet.reshape((-1, len(pokerEngine.infoSet)))
    sess.run(optimizer, feed_dict={Y: Yar, infoState: infosetAr})
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




