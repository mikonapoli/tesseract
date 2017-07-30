import unittest


class TestExample(unittest.TestCase):
    def test_unit_testing_works(self):
        very_true = True
        very_false = False
        self.assertEqual(very_false, False)
        self.assertNotEqual(very_false, very_true)
