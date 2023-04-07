import unittest

from model.bank_controller import BankController
from model.token_array import TokenArray
from model.utils.exception import NotEnoughTokens, TooMuchBankTokens, InvalidTakeTokenAction


class Test_BankController(unittest.TestCase):
    def test_initialisation(self):
        bc = BankController(4)
        bc.__init__(4)
        self.assertIsInstance(bc.bank, TokenArray)
        self.assertEqual(bc.bank.tokens, [7, 7, 7, 7, 7, 5])

        bc.__init__(3)
        self.assertEqual(bc.bank.tokens, [5, 5, 5, 5, 5, 5])

        bc.__init__(2)
        self.assertEqual(bc.bank.tokens, [4, 4, 4, 4, 4, 5])

    def test_withdraw(self):
        bc = BankController(2)
        bc.__init__(4)

        bc.withdraw(TokenArray([1, 1, 1, 0, 0, 0]))
        self.assertEqual(bc.bank.tokens, [6, 6, 6, 7, 7, 5])
        bc.withdraw(TokenArray([2, 0, 0, 0, 0, 0]))
        self.assertEqual(bc.bank.tokens, [4, 6, 6, 7, 7, 5])
        self.assertEqual(bc.withdraw(TokenArray([2, 0, 0, 0, 0, 0])), None)
        self.assertEqual(bc.bank.tokens, [2, 6, 6, 7, 7, 5])

        self.assertIsInstance(bc.withdraw(TokenArray([0, 0, 0, 0, 0, 1])), InvalidTakeTokenAction)
        self.assertIsInstance(bc.withdraw(TokenArray([0, 0, 0, 0, 0, 0])), InvalidTakeTokenAction)
        self.assertIsInstance(bc.withdraw(TokenArray([1, 0, 0, 0, 0, 0])), InvalidTakeTokenAction)
        self.assertIsInstance(bc.withdraw(TokenArray([1, 1, 0, 0, 0, 0])), InvalidTakeTokenAction)
        self.assertIsInstance(bc.withdraw(TokenArray([2, 0, 0, 0, 0, 0])), InvalidTakeTokenAction)
        self.assertIsInstance(bc.withdraw(TokenArray([1, 2, 0, 0, 0, 0])), InvalidTakeTokenAction)
        self.assertIsInstance(bc.withdraw(TokenArray([1, 1, 1, 1, 0, 0])), InvalidTakeTokenAction)

        bc.withdraw(TokenArray([1, 1, 1, 0, 0, 0]))
        bc.withdraw(TokenArray([1, 1, 1, 0, 0, 0]))
        self.assertIsInstance(bc.withdraw(TokenArray([1, 1, 1, 0, 0, 0])), NotEnoughTokens)

    def test_deposit(self):
        bc = BankController(2)
        bc.__init__(2)
        self.assertIsInstance(bc.deposit(TokenArray([1, 0, 0, 0, 0, 0])), TooMuchBankTokens)

        bc.__init__(2)
        bc.withdraw(TokenArray([1, 1, 1, 0, 0, 0]))
        bc.deposit(TokenArray([1, 1, 1, 0, 0, 0]))
        self.assertEqual(bc.bank.tokens, [4, 4, 4, 4, 4, 5])


if __name__ == '__main__':
    unittest.main()
