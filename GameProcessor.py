import numpy as np

R, P, S = 0, 1, 2
Moves = {"R", "P", "S"}
Tr = {'R': R, 'P': P, 'S': S}

Results = {'PLAYER_1': 1, 'PLAYER_2': 2, 'DRAW': 0}

PayoffMatrix = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])

def GetMoveResult(Player1Move, Player2Move):
    Player1payoff = PayoffMatrix[Tr[Player1Move], Tr[Player2Move]]
    if(Player1payoff == 1):
        return Results['PLAYER_1']
    elif(Player1payoff == 0):
        return Results['DRAW']
    else:
        return Results['PLAYER_2']

def GetPayoff(Player1Move, Player2Move):
    Player1payoff = PayoffMatrix[Player1Move, Player2Move]
    return Player1payoff

# print(GetMoveResult("R", 'P'))
# print(GetMoveResult("R", 'R'))
# print(GetMoveResult("P", 'R'))
# print(GetMoveResult("S", 'P'))