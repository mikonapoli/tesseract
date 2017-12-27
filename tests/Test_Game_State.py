import unittest
from tesseract.Game import Game, RunningState


class TestGame(unittest.TestCase):
    def test_new_game_has_state_running(self):
        g = Game()
        self.assertEqual(g.state.name, "RUNNING")


class TestRunningState(unittest.TestCase):
    def test_running_state_name(self):
        rs = RunningState()
        self.assertEqual(rs.name, "RUNNING")
