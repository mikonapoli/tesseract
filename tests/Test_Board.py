import unittest
from tesseract.well import Well


class TestNewWell(unittest.TestCase):
    def test_size(self):
        well = Well(3, 3)
        well_size = well.get_size()
        self.assertEqual((3, 3), well_size)

    def test_is_empty(self):
        b = Well(3, 3)
        self.assertTrue(b.is_empty())

    def test_height(self):
        well = Well(5, 3)
        self.assertEqual(well.get_height(), 5)

    def test_width(self):
        well = Well(5, 9)
        self.assertEqual(well.get_width(), 9)


class TestWell(unittest.TestCase):
    def test_get_size_returns_size_of_well_map(self):
        well = Well(2, 2)
        well.stack = [[0, 0],
                      [0, 0],
                      [0, 0]]
        well_size = well.get_size()
        self.assertEqual((3, 2), well_size)

    def test_full_well_is_not_empty(self):
        well = Well(2, 2)
        well.stack = [[1, 0],
                      [1, 1],
                      [0, 0]]
        self.assertFalse(well.is_empty())
