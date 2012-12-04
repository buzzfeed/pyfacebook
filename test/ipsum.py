import unittest
import pybzfp

class TestIpsum(unittest.TestCase):
    def test_ipsum(self):
        self.assertEquals('awesome', pybzfp.ipsum())
