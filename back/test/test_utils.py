from unittest import TestCase
<<<<<<< HEAD:back/test/test_utils.py
import utils.parsing as parsing
=======
from back import model as parsing
>>>>>>> e1bf1cc7faf767d6f5e7aa1d5cfa3ede46ef9a85:back/model/test/test_utils.py


class Test(TestCase):
    def test_retrieve_and_parse_cards(self):
        self.assertEqual(len(parsing.retrieve_and_parse_cards()), 90)
