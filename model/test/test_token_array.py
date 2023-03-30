from unittest import TestCase
from typing import List

from model.token_array import TokenArray


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

    def test_isub(self):
        ta1 = TokenArray([2, 2, 2, 2, 2, 2])
        ta2 = TokenArray([1, 1, 1, 1, 1, 1])
        ta1 -= ta2
        self.assertEqual(ta1, TokenArray([1, 1, 1, 1, 1, 1]))

    def test_ge(self):
        ta1 = TokenArray([2, 2, 2, 2, 2, 2])
        ta2 = TokenArray([1, 1, 1, 1, 1, 1])
        self.assertTrue(ta1 >= ta2)
        self.assertFalse(ta2 >= ta1)
        ta3 = TokenArray([2, 2, 2, 2, 0, 2])
        self.assertTrue(ta3 >= ta1)
