import unittest

from model.bank_controller import BankController
from model.token_array import TokenArray
from utils.exception import NotEnoughTokens, TooMuchBankTokens


class Test_BankController(unittest.TestCase):
    def test_initialisation(self):
        bc = BankController(4)
        self.assertIsInstance(bc.bank, TokenArray)
        self.assertEqual(bc.bank.get_tokens(), [7, 7, 7, 7, 7, 5])

        bc = BankController(3)
        self.assertEqual(bc.bank.get_tokens(), [5, 5, 5, 5, 5, 5])

        bc = BankController((2))
        self.assertEqual(bc.bank.get_tokens(), [4, 4, 4, 4, 4, 5])

    def test_withdraw(self):
        bc = BankController(4)

        bc.withdraw(TokenArray([1, 1, 1, 0, 0, 0]))
        self.assertEqual(bc.bank.get_tokens(), [6, 6, 6, 7, 7, 5])
        bc.withdraw(TokenArray([2, 0, 0, 0, 0, 0]))
        self.assertEqual(bc.bank.get_tokens(), [4, 6, 6, 7, 7, 5])
        self.assertEqual(bc.withdraw(TokenArray([2, 0, 0, 0, 0, 0])), None)
        self.assertEqual(bc.bank.get_tokens(), [2, 6, 6, 7, 7, 5])
        self.assertEqual(bc.withdraw(TokenArray([0, 0, 0, 0, 0, 1])), None)
        self.assertEqual(bc.bank.get_tokens(), [2, 6, 6, 7, 7, 4])

        # self.assertIsInstance(bc.withdraw(TokenArray([0, 0, 0, 0, 0, 0])), InvalidTakeTokenAction)
        # self.assertIsInstance(bc.withdraw(TokenArray([1, 0, 0, 0, 0, 0])), InvalidTakeTokenAction)
        # self.assertIsInstance(bc.withdraw(TokenArray([1, 1, 0, 0, 0, 0])), InvalidTakeTokenAction)
        # self.assertIsInstance(bc.withdraw(TokenArray([2, 0, 0, 0, 0, 0])), InvalidTakeTokenAction)
        # self.assertIsInstance(bc.withdraw(TokenArray([1, 2, 0, 0, 0, 0])), InvalidTakeTokenAction)
        # self.assertIsInstance(bc.withdraw(TokenArray([1, 1, 1, 1, 0, 0])), InvalidTakeTokenAction)

        bc.withdraw(TokenArray([1, 1, 1, 0, 0, 0]))
        bc.withdraw(TokenArray([1, 1, 1, 0, 0, 0]))
        self.assertIsInstance(bc.withdraw(
            TokenArray([1, 1, 1, 0, 0, 0])), NotEnoughTokens)

    def test_deposit(self):
        bc = BankController(2)
        self.assertIsInstance(bc.deposit(TokenArray(
            [1, 0, 0, 0, 0, 0])), TooMuchBankTokens)

        bc = BankController(2)
        bc.withdraw(TokenArray([1, 1, 1, 0, 0, 0]))
        bc.deposit(TokenArray([1, 1, 1, 0, 0, 0]))
        self.assertEqual(bc.bank.get_tokens(), [4, 4, 4, 4, 4, 5])


if __name__ == '__main__':
    unittest.main()
