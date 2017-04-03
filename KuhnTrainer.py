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
numpy.random.seed(12)

def Normalise(v):
    norm=np.linalg.norm(v, ord=1)
    if norm==0:
        norm=np.finfo(v.dtype).eps
    return v/norm

def MakeChoise(dist, batchSize):
    dist = Normalise(dist)
    return np.random.choice(len(dist), batchSize, p=dist)

# Parameters
learning_rate = 0.01
training_epochs = 1000
display_step = 50
SAMPLE_SIZE = 1

INPUT_SIZE = 3 # Max - three possible moves
OUTPUT_SIZE = 2 # Two actions: pass, bet

alpha = 0.3

# Network Parameters
n_hidden_1 = 256 # 1st layer number of features
n_hidden_2 = 256 # 2nd layer number of features

# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([INPUT_SIZE, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, OUTPUT_SIZE]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([OUTPUT_SIZE]))
}

infoState = tf.placeholder("float", [INPUT_SIZE])

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
    Y = tf.placeholder(tf.float32, [OUTPUT_SIZE])

    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels = Y, logits = pred)
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)
    init = tf.global_variables_initializer()

    pokerEngine = KuhnPoker()

    with tf.Session() as sess:
        sess.run(init)
        for epoch in range(training_epochs):
            p1MovesProbs = sess.run(pred, feed_dict={infoState: pokerEngine.infoSet})
            p1Moves = MakeChoise(p1MovesProbs, SAMPLE_SIZE)
            for p1move in p1Moves:

                p2MovesProbs = sess.run(pred, feed_dict={infoState: pokerEngine.infoSet})

            opMove = GetNextOpMove(SAMPLE_SIZE)

            results = []
            for i in range(SAMPLE_SIZE):
                chosenMove = nnMove[i]
                payoff = GameProcessor.GetPayoff(chosenMove, opMove[i])
                newMoveProb = predictedProbability[chosenMove]  + predictedProbability[chosenMove] * payoff * alpha
                predictedProbability[chosenMove] = newMoveProb
                predictedProbability = Normalise(predictedProbability)

            sess.run(optimizer, feed_dict={Y: predictedProbability})


        newPred = sess.run(pred)
        print(newPred)


def BatchSubSamples(pokerEngine):
    infosetBackup = pokerEngine.infoSet.copy()
    pokerEngineMoveId = pokerEngine.currentMoveId

    movesProbabileties = [0.33, 0.33]
    moveIds = MakeChoise(movesProbabileties, SAMPLE_SIZE)


    totalPayoff = 0
    for moveId in moveIds:
        oneHotMove = MovesToOneHot[moveId + 1]
        pokerEngine.MakeOneHotMove(oneHotMove)
        if(pokerEngine.IsTerminateState()):
            totalPayoff += pokerEngine.GetPayoff(Players.one)
        else:
            totalPayoff += BatchSubSamples(pokerEngine)

        pokerEngine.infoSet = infosetBackup.copy()
        pokerEngine.currentMoveId = pokerEngineMoveId

    return totalPayoff

def RndGame(pokerEngine):
    if (bool(random.getrandbits(1))):
        pokerEngine.MakeMove(Moves.bet)
    else:
        pokerEngine.MakeMove(Moves.pas)

    if (pokerEngine.IsTerminateState()):
        return pokerEngine.GetPayoff(Players.one)
    else:
        return RndGame(pokerEngine)

def UpdateSubGraph(sess, pred, pokerEngine):
    p1MovesProbs = sess.run(pred, feed_dict={infoState: pokerEngine.infoSet})
    p1Moves = MakeChoise(p1MovesProbs, SAMPLE_SIZE)
    for p1move in p1Moves:
        newPokerEngine = copy.deepcopy(pokerEngine)
        newPokerEngine.MakeOneHotMove(p2move)

        p2MovesProbs = sess.run(pred, feed_dict={infoState: pokerEngine.infoSet})
        p2Moves = MakeChoise(p2MovesProbs, SAMPLE_SIZE)
        for p2move in p2Moves:
            newPokerEngine = copy.deepcopy(pokerEngine)
            newPokerEngine.MakeOneHotMove(p2move)




if __name__ == '__main__':

    pokerEngine = KuhnPoker()
    # totalPayoff = 0
    #
    # for _ in range(2000):
    #     totalPayoff += RndGame(pokerEngine)
    #     pokerEngine.NewRound()

    totalPayoff = 0
    for _ in range(1000):
        currentPayoff = SamplePlayerMoves2(pokerEngine)
        totalPayoff += currentPayoff
        #print(pokerEngine.cards, currentPayoff)
        pokerEngine.NewRound()

    print("Total: ", totalPayoff)




