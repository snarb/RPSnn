import unittest
from KuhnPoker import KuhnPoker, Players, Moves, Results

class TestStringMethods(unittest.TestCase):
    def test_one(self):
        kn = KuhnPoker()
        kn.MakeMove(Moves.pas)

        self.assertTrue(kn.infoSet[0] == Moves.pas.value)
        self.assertTrue(not kn.IsTerminateState())

        kn.MakeMove(Moves.pas)
        self.assertTrue(kn.infoSet[1] == Moves.pas.value)
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
        kn = KuhnPoker()

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
        kn = KuhnPoker()

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
        kn = KuhnPoker()

        kn.MakeMove(Moves.bet)
        self.assertTrue(not kn.IsTerminateState())
        kn.MakeMove(Moves.pas)
        self.assertTrue(kn.IsTerminateState())

        kn.cards = [1, 2, 3]
        self.assertTrue(kn.GetPayoff(player=Players.one) == 1)
        kn.cards = [2, 1, 3]
        self.assertTrue(kn.GetPayoff(player=Players.one) == 1)


    def test_five(self):
        kn = KuhnPoker()

        kn.MakeMove(Moves.bet)
        self.assertTrue(not kn.IsTerminateState())
        kn.MakeMove(Moves.bet)
        self.assertTrue(kn.IsTerminateState())

        kn.cards = [1, 2, 3]
        self.assertTrue(kn.GetPayoff(player=Players.one) == -2)
        kn.cards = [2, 1, 3]
        self.assertTrue(kn.GetPayoff(player=Players.one) == 2)


    def test_prev_infoset(self):
        kn = KuhnPoker()
        infoset = kn.GetPrevInfoset(Players.one)


if __name__ == '__main__':
    unittest.main()