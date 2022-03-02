import os
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image
from abc import abstractmethod

class Downsampler(object):
    def __init__(self, factor, degradation_kernel_size):
        self.factor = factor
        self.degradation_kernel_size = degradation_kernel_size

    def _create_lowres(self, highres):
        self.__debug_14bit(highres, 'img')
        result = self._degrade(highres)
        self.__debug_14bit(result, 'img_degraded')
        result = self._direct_downsample(result)
        self.__debug_14bit(result, 'img_downsampled')
        result = self._noise(result)
        return result

    def downsample(self, scene_path, num_lrs):
        assert num_lrs < 1000
        hr_path = os.path.join(scene_path, 'HR.png')  # TODO: could support other formats here
        ground_truth = Image.fromarray(np.array(Image.open(hr_path)).astype("uint16"))
        for i in range(num_lrs):
            filename = f'LR{i:03}.png'
            lr_path = os.path.join(scene_path, filename)
            lr = self._create_lowres(ground_truth)
            lr.save(lr_path)

    def __debug_14bit(self, img, title=None):
        img_tmp = np.asarray(img)
        img_tmp = img_tmp * 4
        Image.fromarray(img_tmp).show(title)

    @abstractmethod
    def _degrade(self, img):
        raise NotImplementedError()

    @abstractmethod
    def _direct_downsample(self, img):
        raise NotImplementedError()

    @abstractmethod
    def _noise(self, img):
        raise NotImplementedError()

class BicubicDownsampler(Downsampler):
    def __init__(self, factor, degradation_kernel_size):
        super().__init__(factor, degradation_kernel_size)

    def _degrade(self, img):
        img_blurred = gaussian_filter(img, sigma=self.degradation_kernel_size)
        return Image.fromarray(img_blurred)

    def _direct_downsample(self, img):
        lr_size = (int(img.size[0] / self.factor), int(img.size[1] / self.factor))
        img = img.convert('I')
        img = img.resize(lr_size, Image.BICUBIC)
        img = img.convert('I;16')
        return img

    def _noise(self, img):
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                cur_val = img.get_pixel((i, j))
                print(cur_val)
        return img  # TODO
