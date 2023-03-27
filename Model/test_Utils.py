from unittest import TestCase
import Utils
class Test(TestCase):
    def test_retrieve_and_parse_cards(self):
        self.assertEqual(len(Utils.retrieve_and_parse_cards()), 90)