import unittest

from model.bank_controller import BankController
from model.token_array import TokenArray
from model.utils.exception import NotEnoughTokens, TooMuchBankTokens


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

        bc.withdraw(TokenArray([7, 7, 7, 7, 7, 5]))
        self.assertEqual(bc.bank.tokens, [0, 0, 0, 0, 0, 0])

        bc.__init__(2)
        self.assertIsInstance(bc.withdraw(TokenArray([5, 0, 0, 0, 0, 0])), NotEnoughTokens)

    def test_deposit(self):
        bc = BankController(2)
        bc.__init__(2)
        self.assertIsInstance(bc.deposit(TokenArray([1, 0, 0, 0, 0, 0])), TooMuchBankTokens)


if __name__ == '__main__':
    unittest.main()
