from unittest import TestCase
from back import model as parsing


class Test(TestCase):
    def test_retrieve_and_parse_cards(self):
        self.assertEqual(len(parsing.retrieve_and_parse_cards()), 90)
