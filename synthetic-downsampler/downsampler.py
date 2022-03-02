import os
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image
from abc import abstractmethod

class Downsampler(object):
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.__log_pipeline_stages()

    def _create_lowres(self, highres):
        result = highres
        # transform the image through all pipeline stages
        for action, config in self.pipeline:
            result = action(self, result, **config)
        if result.size[0] != 128 or result.size[1] != 128:
            print(f'WARN: resulting image has unexpected size {result.size}')
        return result

    def downsample(self, scene_path, num_lrs):
        assert num_lrs < 1000
        hr_path = os.path.join(scene_path, 'HR.png')
        ground_truth = Image.fromarray(np.array(Image.open(hr_path)).astype("uint16"))
        for i in range(num_lrs):
            filename = f'LR{i:03}.png'
            lr_path = os.path.join(scene_path, filename)
            lr = self._create_lowres(ground_truth)
            lr.save(lr_path)

    def __log_pipeline_stages(self):
        conf = '******************************'
        conf += '*** DOWNSAMPLING PIPELINE: ***'
        conf += '******************************\n'
        size = 384
        for action, config in self.pipeline:
            conf += f'       size=({size}, {size}), action={action.__name__:<20}, params={config}'
            if action.__name__ == '_direct_downsample':
                size = int(size / config['factor'])
        conf += f'  OUT: size=({size}, {size})'
        conf += '\n******************************\n'
        return conf

    def __debug_14bit(self, img, title=None):
        img_tmp = np.asarray(img)
        img_tmp = img_tmp * 4
        Image.fromarray(img_tmp).show(title)

    @abstractmethod
    def _degrade(self, img, sigma):
        raise NotImplementedError()

    @abstractmethod
    def _direct_downsample(self, img, factor):
        raise NotImplementedError()

    @abstractmethod
    def _noise(self, img, sigma):
        raise NotImplementedError()

class BicubicDownsampler(Downsampler):
    def __init__(self, pipeline):
        super().__init__(pipeline)

    def _degrade(self, img, sigma):
        img_blurred = gaussian_filter(img, sigma=sigma)
        return Image.fromarray(img_blurred)

    def _direct_downsample(self, img, factor):
        lr_size = (int(img.size[0] / factor), int(img.size[1] / factor))
        img = img.convert('I')
        img = img.resize(lr_size, Image.BICUBIC)
        img = img.convert('I;16')
        return img

    def _noise(self, img, sigma):
        noise = np.random.normal(0, sigma, (img.size[0],img.size[1]))
        img = np.clip(np.asarray(img) + noise, 0.0, 2**16-1)
        return Image.fromarray(img.round().astype('uint16'))
