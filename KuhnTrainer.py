import tensorflow as tf
import numpy
import GameProcessor
import matplotlib.pyplot as plt
rng = numpy.random
import numpy as np
from sklearn.preprocessing import normalize

def Normalise(v):
    norm=np.linalg.norm(v, ord=1)
    if norm==0:
        norm=np.finfo(v.dtype).eps
    return v/norm

def MakeChoise(dist, batchSize):
    dist = Normalise(dist)
    return np.random.choice(len(dist), batchSize, p=dist)


def GetNextOpMove(batchSize):
    return MakeChoise(OPP_STRATEGY, batchSize)

# Parameters
learning_rate = 0.01
training_epochs = 1000
display_step = 50
BATCH_SIZE = 1
TESTS_COUNT = 100
shape = [3]

alpha = 0.3

b = tf.Variable(tf.ones(shape), name="bias")
pred = tf.nn.softmax(b) # Add variable for optimisation to second graph ?!
Y = tf.placeholder(tf.float32, shape)
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels = Y, logits = pred)
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cross_entropy)
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    for epoch in range(training_epochs):
        predictedProbability = sess.run(pred)
        opMove = GetNextOpMove(TESTS_COUNT)
        nnMove = MakeChoise(predictedProbability, TESTS_COUNT)

        results = []
        for i in range(TESTS_COUNT):
            chosenMove = nnMove[i]
            payoff = GameProcessor.GetPayoff(chosenMove, opMove[i])
            newMoveProb = predictedProbability[chosenMove]  + predictedProbability[chosenMove] * payoff * alpha
            predictedProbability[chosenMove] = newMoveProb
            predictedProbability = Normalise(predictedProbability)

        sess.run(optimizer, feed_dict={Y: predictedProbability})


    newPred = sess.run(pred)
    print(newPred)


