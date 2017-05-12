import numpy as np

def Normalise(v):
    if(not np.any(v)):
        v.fill(1 / len(v))
        return v

    norm=np.linalg.norm(v, ord=1)
    if norm==0:
        norm=np.finfo(v.dtype).eps
    return v/norm

def MakeChoise(dist, batchSize):
   #return np.array([0,1,0,1])
   return np.random.choice(len(dist), batchSize, p=dist)

def MakeNormChoise(dist, batchSize):
    dist = Normalise(dist)
    return MakeChoise(dist, batchSize)


def IsClose(real, target, tolerance):
        dif = abs(real - target)
        return dif <= tolerance

def IsPlayerTwoCloseToNash(playerTwoTree, tolerance = 0.5):
        playerTwoStrategy = playerTwoTree['1 | bet;uplayed;uplayed'].data.GetAverageStrategy()
        if(not IsClose(playerTwoStrategy[1], 0.0, tolerance)): # when having a Jack, never calling
            return False

        playerTwoStrategy = playerTwoTree['1 | pas;uplayed;uplayed'].data.GetAverageStrategy()
        if(not IsClose(playerTwoStrategy[1], 1/3, tolerance)): # when having a Jack, betting with the probability of 1/3
            return False

        playerTwoStrategy = playerTwoTree['2 | pas;uplayed;uplayed'].data.GetAverageStrategy()
        if(not IsClose(playerTwoStrategy[0], 1.0, tolerance)): # when having a Queen, checking if possible
            return False

        playerTwoStrategy = playerTwoTree['2 | bet;uplayed;uplayed'].data.GetAverageStrategy()
        if(not IsClose(playerTwoStrategy[1], 1/3, tolerance)): # otherwise calling with the probability of 1/3
            return False

        playerTwoStrategy = playerTwoTree['3 | pas;uplayed;uplayed'].data.GetAverageStrategy()
        if (not IsClose(playerTwoStrategy[0], 0.0, tolerance)):  # Always betting or calling when having a King
            return False

        playerTwoStrategy = playerTwoTree['3 | bet;uplayed;uplayed'].data.GetAverageStrategy()
        if (not IsClose(playerTwoStrategy[1], 1.0, tolerance)):  # Always betting or calling when having a King
            return False

        return True


def IsPlayerTwoCloseToNash(playerTwoTree, tolerance=0.5):
    playerTwoStrategy = playerTwoTree['1 | bet;uplayed;uplayed'].data.GetAverageStrategy()
    if (not IsClose(playerTwoStrategy[1], 0.0, tolerance)):  # when having a Jack, never calling
        return False

    playerTwoStrategy = playerTwoTree['1 | pas;uplayed;uplayed'].data.GetAverageStrategy()
    if (not IsClose(playerTwoStrategy[1], 1 / 3, tolerance)):  # when having a Jack, betting with the probability of 1/3
        return False

    playerTwoStrategy = playerTwoTree['2 | pas;uplayed;uplayed'].data.GetAverageStrategy()
    if (not IsClose(playerTwoStrategy[0], 1.0, tolerance)):  # when having a Queen, checking if possible
        return False

    playerTwoStrategy = playerTwoTree['2 | bet;uplayed;uplayed'].data.GetAverageStrategy()
    if (not IsClose(playerTwoStrategy[1], 1 / 3, tolerance)):  # otherwise calling with the probability of 1/3
        return False

    playerTwoStrategy = playerTwoTree['3 | pas;uplayed;uplayed'].data.GetAverageStrategy()
    if (not IsClose(playerTwoStrategy[0], 0.0, tolerance)):  # Always betting or calling when having a King
        return False

    playerTwoStrategy = playerTwoTree['3 | bet;uplayed;uplayed'].data.GetAverageStrategy()
    if (not IsClose(playerTwoStrategy[1], 1.0, tolerance)):  # Always betting or calling when having a King
        return False

    return True