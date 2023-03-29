from unittest import TestCase
import model.utils as utils


class Test(TestCase):
    def test_retrieve_and_parse_cards(self):
        self.assertEqual(len(utils.retrieve_and_parse_cards()), 90)
