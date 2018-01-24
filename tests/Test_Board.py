import unittest
from tesseract.board import Board


class TestNewBoard(unittest.TestCase):
    def test_size(self):
        board = Board(3, 3)
        board_size = board.get_size()
        self.assertEqual((3, 3), board_size)

    def test_is_empty(self):
        b = Board(3, 3)
        self.assertTrue(b.is_empty())


class TestBoard(unittest.TestCase):
    def test_get_size_returns_size_of_board_map(self):
        board = Board(2, 2)
        board.map = [[0, 0],
                     [0, 0],
                     [0, 0]]
        board_size = board.get_size()
        self.assertEqual((3, 2), board_size)

    def test_full_board_is_not_empty(self):
        board = Board(2, 2)
        board.map = [[1, 0],
                     [1, 1],
                     [0, 0]]
        self.assertFalse(board.is_empty())
