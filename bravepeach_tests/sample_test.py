import unittest2 as unittest


class SampleTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_sample(self):
        self.assertEqual(2, 1+1)
