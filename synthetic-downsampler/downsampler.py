import os
from PIL import Image

class Downsampler(object):
    def __init__(self, factor):
        self.factor = factor

    def _create_lowres(self, highres):
        raise NotImplementedError()

    def downsample(self, scene_path, num_lrs):
        assert num_lrs < 1000
        hr_path = os.path.join(scene_path, 'HR.png')  # TODO: could support other formats here
        ground_truth = Image.open(hr_path)
        for i in range(num_lrs):
            filename = f'LR{i:03}.png'
            lr_path = os.path.join(scene_path, filename)
            lr = self._create_lowres(ground_truth)
            lr.save(lr_path)

class BicubicDownsampler(Downsampler):
    def __init__(self, factor):
        super().__init__(factor)

    def _create_lowres(self, highres):
        lr_size = (int(highres.size[0] / self.factor), int(highres.size[1] / self.factor))
        return highres.resize(lr_size, Image.BICUBIC)
