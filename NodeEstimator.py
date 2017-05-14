import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation
#from keras.wrappers.scikit_learn import KerasRegressor
#from sklearn.metrics import mean_squared_error
from keras import optimizers

BATCH_SIZE = 5
SAMPLES = 2000
EPOCHS = 1
INPUT_SIZE = 2 # Two actions

class Estimator:

    def __init__(self):
        model = Sequential()
        model.add(Dense(5, input_dim=INPUT_SIZE, kernel_initializer='normal', activation='relu'))
        model.add(Dense(7, kernel_initializer='normal', activation='relu'))
        model.add(Dense(1, kernel_initializer='normal'))
        #sgd = optimizers.SGD(lr=0.01, momentum=0.9, nesterov=True)
        adam = optimizers.Adam(lr=0.05)

        model.compile(loss='mean_squared_error', optimizer='adam')
        self.model = model


    def Train(self, strategies, utils):
        # x_train = np.random.random_sample((SAMPLES, BATCH_SIZE)) / 2
        # y_train = x_train  * x_train
        #
        #
        # x_test = np.random.random_sample((SAMPLES, BATCH_SIZE)) / 2
        # y_test = x_test  * x_test
        testL = int(len(strategies) * 0.9)
        x_train = np.array(strategies[:testL]).reshape(testL, INPUT_SIZE)
        y_train = np.array(utils[:testL]) / 2

        x_test = np.array(strategies[testL:]).reshape(-1, INPUT_SIZE)
        y_test = np.array(utils[testL:]) / 2

        self.model.fit(x_train, y_train, epochs=5, batch_size=BATCH_SIZE)

        # self.model.fit(x_train[:150], y_train[:150], epochs=5, batch_size=BATCH_SIZE)
        # self.model.fit(x_train[150:], y_train[150:], epochs=10, batch_size=BATCH_SIZE)

        score = self.model.evaluate(x_test, y_test, batch_size=BATCH_SIZE)

        # estimator = KerasRegressor(build_fn=baseline_model, epochs=5, batch_size=BATCH_SIZE, verbose=1)
        # estimator.fit(input_data, target)

        #loss_and_metrics = estimator.evaluate(x_test, y_test, batch_size=128)
        classes = self.model.predict(x_test)
        # print(x_test[0], classes[0])
        #score = mean_squared_error(y_test, estimator.predict(x_test))

        print("score is: ",  score)
        #0.1278


