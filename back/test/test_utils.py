from utils.parsing import retrieve_and_parse_cards
from unittest import TestCase

class Test(TestCase):
    def test_retrieve_and_parse_cards(self):
        self.assertEqual(len(retrieve_and_parse_cards()), 90)
