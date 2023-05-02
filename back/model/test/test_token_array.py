from unittest import TestCase
from typing import List

from back.model import TokenArray, Color
from back.model import NotEnoughTokens


class Test_TokenArray(TestCase):
    def test_initialization(self):
        ta = TokenArray()
        self.assertIsInstance(ta, TokenArray)
        self.assertIsInstance(ta.get_tokens(), List)
        self.assertEqual(len(ta.get_tokens()), 6)

    def test_withdraw_token(self):
        ta = TokenArray([2, 2, 2, 2, 2, 2])
        ta.withdraw_token(Color.WHITE, 1)
        self.assertEqual(ta.get_tokens(), [1, 2, 2, 2, 2, 2])
        self.assertIsInstance(ta.withdraw_token(
            Color.WHITE, 2), NotEnoughTokens)

    def test_withdraw_tokens(self):
        ta = TokenArray([2, 2, 2, 2, 2, 2])
        ta.withdraw_tokens(TokenArray([1, 1, 1, 1, 0, 0]))
        self.assertEqual(ta.get_tokens(), [1, 1, 1, 1, 2, 2])
        self.assertIsInstance(ta.withdraw_tokens(
            TokenArray([1, 1, 1, 1, 3, 0])), NotEnoughTokens)

    def test_deposit_token(self):
        ta = TokenArray([2, 2, 2, 2, 2, 2])
        ta.deposit_token(Color.WHITE, 1)
        self.assertEqual(ta.get_tokens(), [3, 2, 2, 2, 2, 2])

    def test_deposit_tokens(self):
        ta = TokenArray([2, 2, 2, 2, 2, 2])
        ta.deposit_tokens(TokenArray([1, 1, 1, 1, 0, 0]))
        self.assertEqual(ta.get_tokens(), [3, 3, 3, 3, 2, 2])

    def test_nb_of_tokens(self):
        ta = TokenArray([1, 1, 1, 1, 1, 1])
        self.assertEqual(ta.nb_of_tokens(), 6)

    def test_can_withdraw(self):
        ta = TokenArray([2, 2, 2, 2, 2, 2])
        self.assertTrue(ta.can_withdraw(TokenArray([1, 1, 1, 1, 1, 2])))
        self.assertFalse(ta.can_withdraw(TokenArray([3, 1, 1, 1, 1, 1])))

    def test_can_pay(self):
        ta1 = TokenArray([2, 2, 2, 2, 2, 2])
        ta2 = TokenArray([1, 1, 1, 1, 2, 0])
        self.assertTrue(ta1.can_pay(ta2))

        ta1 = TokenArray([2, 2, 2, 2, 2, 2])
        ta2 = TokenArray([1, 1, 1, 1, 3, 0])
        self.assertTrue(ta1.can_pay(ta2))

    def test_pay(self):
        ta1 = TokenArray([2, 2, 2, 2, 2, 2])
        ta1.pay(TokenArray([1, 1, 1, 1, 3, 0]))
        self.assertEqual(ta1.get_tokens(), [1, 1, 1, 1, 0, 1])

    def test_iadd(self):
        ta1 = TokenArray([2, 2, 2, 2, 2, 2])
        ta2 = TokenArray([1, 1, 1, 1, 1, 1])
        ta1 += ta2
        self.assertEqual(ta1, TokenArray([3, 3, 3, 3, 3, 3]))

    def test_isub(self):
        ta1 = TokenArray([2, 2, 2, 2, 2, 2])
        ta2 = TokenArray([1, 1, 1, 1, 1, 0])
        ta1 -= ta2
        self.assertEqual(ta1.get_tokens(), [1, 1, 1, 1, 1, 2])

        ta1 = TokenArray([2, 2, 2, 2, 2, 2])
        ta2 = TokenArray([1, 1, 1, 1, 2, 1])
        ta1 -= ta2
        self.assertEqual(ta1.get_tokens(), [1, 1, 1, 1, 0, 1])

    def test_add(self):
        ta1 = TokenArray([2, 2, 2, 2, 2, 2])
        ta2 = TokenArray([2, 2, 2, 2, 2, 2])
        self.assertEqual((ta1 + ta2).get_tokens(), [4, 4, 4, 4, 4, 4])

    def test_sub(self):
        ta1 = TokenArray([3, 3, 3, 3, 3, 3])
        ta2 = TokenArray([2, 2, 2, 2, 2, 2])
        self.assertEqual((ta1 - ta2).get_tokens(), [1, 1, 1, 1, 1, 1])

    def test_ge(self):
        ta1 = TokenArray([3, 3, 3, 3, 3, 3])
        ta2 = TokenArray([2, 2, 2, 2, 2, 2])
        self.assertTrue(ta1 >= ta2)
        self.assertTrue(ta1 >= ta1)
        self.assertFalse(ta2 >= ta1)

    def test_le(self):
        ta1 = TokenArray([2, 2, 2, 2, 2, 2])
        ta2 = TokenArray([3, 3, 3, 3, 3, 3])
        self.assertTrue(ta1 <= ta2)
        self.assertTrue(ta1 <= ta1)
        self.assertFalse(ta2 <= ta1)
