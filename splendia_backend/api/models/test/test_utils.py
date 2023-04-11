from unittest import TestCase
import models.utils.parsing as parsing


class Test(TestCase):
    def test_retrieve_and_parse_cards(self):
        self.assertEqual(len(parsing.retrieve_and_parse_cards()), 90)
