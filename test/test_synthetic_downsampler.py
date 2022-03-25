import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")
from synthetic_downsampler.check_synthetic import *

class TestIsAuthenticLR(unittest.TestCase):
    def test_identical(self):
        self.assertTrue(is_authentic_lr(
            auth_lr='test/data/authentic/train/NIR/imgset0594/LR008.png',
            lr='test/data/authentic/train/NIR/imgset0594/LR008.png',
        ))

    def test_different(self):
        self.assertFalse(is_authentic_lr(
            auth_lr='test/data/authentic/train/NIR/imgset0594/LR008.png',
            lr='test/data/synth100_0/train/NIR/imgset0594/LR008.png',
        ))

if __name__ == '__main__':
    unittest.main()