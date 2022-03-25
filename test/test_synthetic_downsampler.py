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

class TestIsSyntheticScene(unittest.TestCase):
    def test_identical(self):
        self.assertFalse(is_synthetic_scene(
            auth_scene='test/data/authentic/train/NIR/imgset0594',
            scene='test/data/authentic/train/NIR/imgset0594',
        ))

    def test_different(self):
        self.assertTrue(is_synthetic_scene(
            auth_scene='test/data/authentic/train/NIR/imgset0594',
            scene='test/data/synth100_0/train/NIR/imgset0594',
        ))

class TestIsSyntheticDirectory(unittest.TestCase):
    def test_identical_train(self):
        counts = get_synth_auth_scene_counts(
            auth_root='test/data/authentic/train',
            root='test/data/authentic/train',
        )
        self.assertEqual(counts['auth'], 4)
        self.assertEqual(counts['synth'], 0)

    def test_identical_val(self):
        counts = get_synth_auth_scene_counts(
            auth_root='test/data/authentic/val',
            root='test/data/authentic/val',
        )
        self.assertEqual(counts['auth'], 4)
        self.assertEqual(counts['synth'], 0)

    def test_different_train(self):
        counts = get_synth_auth_scene_counts(
            auth_root='test/data/authentic/train',
            root='test/data/synth100_0/train',
        )
        self.assertEqual(counts['auth'], 0)
        self.assertEqual(counts['synth'], 4)

    def test_different_val(self):
        counts = get_synth_auth_scene_counts(
            auth_root='test/data/authentic/val',
            root='test/data/synth100_0/val',
        )
        self.assertEqual(counts['auth'], 4)
        self.assertEqual(counts['synth'], 0)

class Test50_50(unittest.TestCase):
    def test_different_train(self):
        counts = get_synth_auth_scene_counts(
            auth_root='test/data/authentic/train',
            root='test/data/synth50_50/train',
        )
        self.assertEqual(counts['auth'], 2)
        self.assertEqual(counts['synth'], 2)

    def test_different_val(self):
        counts = get_synth_auth_scene_counts(
            auth_root='test/data/authentic/val',
            root='test/data/synth50_50/val',
        )
        self.assertEqual(counts['auth'], 4)
        self.assertEqual(counts['synth'], 0)

if __name__ == '__main__':
    unittest.main()