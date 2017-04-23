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
   return np.random.choice(len(dist), batchSize, p=dist)

def MakeNormChoise(dist, batchSize):
    dist = Normalise(dist)
    return MakeChoise(dist, batchSize)