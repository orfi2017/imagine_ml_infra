import unittest
from melampus.feature_selector import FeatureSelector


class TestFeatureSelector(unittest.TestCase):
    def test_exceptions(self):
        self.assertRaises(Exception, FeatureSelector(filename=''))
