from unittest import TestCase
from typing import List

from models.token_array import TokenArray


class Test_TokenArray(TestCase):
    def test_initialization(self):
        tokenarray = TokenArray()
        self.assertIsInstance(tokenarray, TokenArray)
        self.assertIsInstance(tokenarray.tokens, List)
        self.assertEqual(len(tokenarray.tokens), 6)

    def test_iadd(self):
        ta1 = TokenArray([2, 2, 2, 2, 2, 2])
        ta2 = TokenArray([1, 1, 1, 1, 1, 1])
        ta1 += ta2
        self.assertEqual(ta1, TokenArray([3, 3, 3, 3, 3, 3]))

    def test_can_pay(self):
        ta1 = TokenArray([2, 2, 2, 2, 2, 2])
        ta2 = TokenArray([1, 1, 1, 1, 2, 0])
        self.assertTrue(ta1.can_pay(ta2))

        ta1 = TokenArray([2, 2, 2, 2, 2, 2])
        ta2 = TokenArray([1, 1, 1, 1, 3, 0])
        self.assertTrue(ta1.can_pay(ta2))

    def test_isub(self):
        ta1 = TokenArray([2, 2, 2, 2, 2, 2])
        ta2 = TokenArray([1, 1, 1, 1, 1, 0])
        ta1 -= ta2
        self.assertEqual(ta1.tokens, [1, 1, 1, 1, 1, 2])

        ta1 = TokenArray([2, 2, 2, 2, 2, 2])
        ta2 = TokenArray([1, 1, 1, 1, 3, 0])
        ta1 -= ta2
        self.assertEqual(ta1.tokens, [1, 1, 1, 1, 0, 1])
