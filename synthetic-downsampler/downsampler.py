import os
from PIL import Image

class Downsampler(object):
    def __init__(self, factor):
        self.factor = factor

    def downsample(self, scene_path, num_lrs):
        raise NotImplementedError()

class BicubicDownsampler(Downsampler):
    def __init__(self, factor):
        super().__init__(factor)

    def downsample(self, scene_path, num_lrs):
        assert num_lrs < 1000
        hr_path = os.path.join(scene_path, 'HR.png')  # TODO: could support other formats here
        ground_truth = Image.open(hr_path)
        lr_size = (int(ground_truth.size[0] / self.factor), int(ground_truth.size[1] / self.factor))
        for i in range(num_lrs):
            filename = f'LR{i:03}.png'
            lr_path = os.path.join(scene_path, filename)
            lr = ground_truth.resize(lr_size, Image.BICUBIC)
            lr.save(lr_path)
