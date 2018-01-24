import unittest
from tesseract.board import Board


class TestNewBoard(unittest.TestCase):
    def test_size(self):
        board = Board(3, 3)
        board_size = board.get_size()
        self.assertEqual((3,3), board_size)




#    def test_is_empty(self):
#        b = Board(3,3)
#        self.assertTrue(b.is_empty())
