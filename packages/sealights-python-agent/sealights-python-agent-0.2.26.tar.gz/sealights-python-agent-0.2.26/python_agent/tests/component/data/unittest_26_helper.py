import unittest


class SanityTestCase(unittest.TestCase):

    def test_3plus3(self):
        assert 3 + 3 == 6

    def test_1plus1(self):
        assert 1 + 1 == 2


class PassErrorTestCase(unittest.TestCase):

    def test_3plus3(self):
        self.assertTrue(3 + 3 == 6)

    def test_1plus1(self):
        self.assertEqual(1 + 1, 2)