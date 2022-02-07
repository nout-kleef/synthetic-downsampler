import glob
import os
from abc import ABC, abstractmethod

class DatasetFormat(ABC):
    def __init__(self, root_path):
        self.root_path = root_path

    @abstractmethod
    def get_scene_paths(self):
        raise NotImplementedError()

class ProbaVFormat(DatasetFormat):
    def __init__(self, root_path):
        super().__init__(root_path=root_path)

    def get_scene_paths(self):
        return glob.glob(os.path.join(self.root_path, 'train', 'RED', 'imgset*')) +\
            glob.glob(os.path.join(self.root_path, 'train', 'NIR', 'imgset*'))
