# test for checker.py

import unittest
from model.business_model.checker import Checker
from model.business_model.token_array import TokenArray


class TestChecker(unittest.TestCase):

    def test_possible_token_to_take_2(self):
        self.assertEqual(
            Checker.possible_token_to_take_2(TokenArray(
                [0, 6, 1, 0, 0, 0]), TokenArray([7, 1, 7, 7, 7, 0])),
            [1, 0, 1, 1, 1, 0])
        self.assertEqual(
            Checker.possible_token_to_take_2(TokenArray(
                [9, 0, 0, 0, 0, 0]), TokenArray([7, 7, 7, 7, 7, 0])),
            [0, 0, 0, 0, 0, 0])
        self.assertEqual(
            Checker.possible_token_to_take_2(TokenArray(
                [6, 0, 2, 1, 0, 0]), TokenArray([7, 7, 2, 7, 7, 0])),
            [0, 0, 0, 0, 0, 0])

    def test_possible_token_to_take_3(self):
        self.assertEqual(
            Checker.possible_token_to_take_3(TokenArray(
                [0, 0, 0, 0, 0, 0]), TokenArray([7, 7, 7, 7, 7, 0])),
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(
            Checker.possible_token_to_take_3(TokenArray(
                [0, 0, 0, 0, 0, 0]), TokenArray([0, 7, 7, 7, 7, 0])),
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1])
        self.assertEqual(
            Checker.possible_token_to_take_3(TokenArray(
                [0, 2, 3, 3, 0, 0]), TokenArray([0, 7, 7, 7, 7, 0])),
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(
            Checker.possible_token_to_take_3(TokenArray(
                [0, 2, 1, 3, 0, 0]), TokenArray([0, 0, 0, 0, 0, 10])),
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(
            Checker.possible_token_to_take_3(TokenArray(
                [2, 1, 2, 3, 4, 1]), TokenArray([0, 0, 0, 0, 0, 0])),
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


if __name__ == '__main__':
    unittest.main()
