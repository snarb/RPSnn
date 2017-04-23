from KuhnPoker import *

class Qlnode:
    def __init__(self, infoset):
        self.infoset = infoset
        self.strategy = np.array([0.5] * NUM_ACTIONS)


