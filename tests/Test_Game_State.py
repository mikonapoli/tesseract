import unittest
from tesseract.Game import Game


class TestGame(unittest.TestCase):
    def test_new_game_has_state(self):
        g = Game()
        self.assertNotEqual(g.state, None)
