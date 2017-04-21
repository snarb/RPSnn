import unittest
from KuhnPoker import KuhnPoker, Players, Moves, Results

class TestStringMethods(unittest.TestCase):
    def CreatePokerEngine(self):
        kn = KuhnPoker()
        kn.NewRound()
        return kn

    def test_one(self):
        kn = self.CreatePokerEngine()

        kn.MakeMove(Moves.pas)
        self.assertTrue(kn.moves[0] == Moves.pas.value)
        self.assertTrue(not kn.IsTerminateState())

        kn.MakeMove(Moves.pas)
        self.assertTrue(kn.moves[1] == Moves.pas.value)
        self.assertTrue(kn.IsTerminateState())

        kn.cards = [1, 2, 3]
        self.assertTrue(kn.GetPayoff(player=Players.one) == -1)
        kn.cards = [2, 1, 3]
        self.assertTrue(kn.GetPayoff(player=Players.one) == 1)
        kn.cards = [3, 2, 1]
        self.assertTrue(kn.GetPayoff(player=Players.one) == 1)
        kn.cards = [2, 3, 1]
        self.assertTrue(kn.GetPayoff(player=Players.one) == -1)
        self.assertTrue(kn.GetPayoff(player=Players.two) == 1)

    def test_two(self):
        kn = self.CreatePokerEngine()

        kn.MakeMove(Moves.pas)
        self.assertTrue(not kn.IsTerminateState())
        kn.MakeMove(Moves.bet)
        self.assertTrue(not kn.IsTerminateState())
        kn.MakeMove(Moves.pas)

        self.assertTrue(kn.IsTerminateState())

        kn.cards = [1, 2, 3]
        self.assertTrue(kn.GetPayoff(player=Players.two) == 1)
        kn.cards = [2, 1, 3]
        self.assertTrue(kn.GetPayoff(player=Players.one) == -1)


    def test_three(self):
        kn = self.CreatePokerEngine()

        kn.MakeMove(Moves.pas)
        self.assertTrue(not kn.IsTerminateState())
        kn.MakeMove(Moves.bet)
        self.assertTrue(not kn.IsTerminateState())
        kn.MakeMove(Moves.bet)

        self.assertTrue(kn.IsTerminateState())

        kn.cards = [1, 2, 3]
        self.assertTrue(kn.GetPayoff(player=Players.one) == -2)
        kn.cards = [2, 1, 3]
        self.assertTrue(kn.GetPayoff(player=Players.one) == 2)

    def test_four(self):
        kn = self.CreatePokerEngine()

        kn.MakeMove(Moves.bet)
        self.assertTrue(not kn.IsTerminateState())
        kn.MakeMove(Moves.pas)
        self.assertTrue(kn.IsTerminateState())

        kn.cards = [1, 2, 3]
        self.assertTrue(kn.GetPayoff(player=Players.one) == 1)
        kn.cards = [2, 1, 3]
        self.assertTrue(kn.GetPayoff(player=Players.one) == 1)


    def test_five(self):
        kn = self.CreatePokerEngine()

        kn.MakeMove(Moves.bet)
        self.assertTrue(not kn.IsTerminateState())
        kn.MakeMove(Moves.bet)
        self.assertTrue(kn.IsTerminateState())

        kn.cards = [1, 2, 3]
        self.assertTrue(kn.GetPayoff(player=Players.one) == -2)
        kn.cards = [2, 1, 3]
        self.assertTrue(kn.GetPayoff(player=Players.one) == 2)


    def test_infoset(self):
        kn = self.CreatePokerEngine()

        infoset = kn.GetInfoset(Players.one)
        prefix1 = str(kn.cards[0]) + " | "
        self.assertTrue(infoset == prefix1 + "uplayed;uplayed;uplayed")

        infoset = kn.GetInfoset(Players.two)
        prefix2 = str(kn.cards[1]) + " | "
        self.assertTrue(infoset == prefix2 + "uplayed;uplayed;uplayed")

        kn.MakeMove(Moves.bet)
        infoset = kn.GetInfoset(Players.one)
        self.assertTrue(infoset == prefix1 + "bet;uplayed;uplayed")

        kn.MakeMove(Moves.pas)
        infoset = kn.GetInfoset(Players.one)
        self.assertTrue(infoset == prefix1 + "bet;pas;uplayed")

        kn.MakeMove(Moves.pas)
        infoset = kn.GetInfoset(Players.one)
        self.assertTrue(infoset == prefix1 + "bet;pas;pas")

    def CheckGetPrevInfosetRaiseIncorrectMoveId(self, kn, player):
        with self.assertRaises(ValueError) as cm:
            kn.GetPrevInfoset(player)

        self.assertTrue('Call in incorrect currentMoveId' in str(cm.exception))

    def test_prev_infoset(self):
        kn = self.CreatePokerEngine()

        infoset = kn.GetPrevInfoset(Players.one)
        self.assertTrue(infoset =="GameTree")

        self.CheckGetPrevInfosetRaiseIncorrectMoveId(kn, Players.two)

        kn.MakeMove(Moves.bet)

        self.CheckGetPrevInfosetRaiseIncorrectMoveId(kn, Players.one)
        infoset = kn.GetPrevInfoset(Players.two)
        self.assertTrue(infoset =="GameTree")

        kn.MakeMove(Moves.bet)

        infoset = kn.GetPrevInfoset( Players.one)
        prefix1 = str(kn.cards[0]) + " | "
        self.assertTrue(infoset == prefix1 + "uplayed;uplayed;uplayed")
        self.CheckGetPrevInfosetRaiseIncorrectMoveId(kn, Players.two)

    def CheckGetLastSubStateRaiseIncorrectMoveId(self, kn, player):
        with self.assertRaises(ValueError) as cm:
            kn.GetLastSubState(player)

        self.assertTrue('Call in incorrect currentMoveId' in str(cm.exception))

    def test_last_sub_set(self):
        kn = self.CreatePokerEngine()

        subState = kn.GetLastSubState(Players.one)
        self.assertTrue(subState == str(kn.cards[0]))

        self.CheckGetLastSubStateRaiseIncorrectMoveId(kn, Players.two)

        kn.MakeMove(Moves.bet)

        subState = kn.GetLastSubState(Players.two)
        self.assertTrue(subState == "2 | bet")
        self.CheckGetLastSubStateRaiseIncorrectMoveId(kn, Players.one)

        kn.MakeMove(Moves.bet)

        subState = kn.GetLastSubState(Players.one)
        self.assertTrue(subState == "bet")

if __name__ == '__main__':
    unittest.main()