import glob
import os
from abc import ABC, abstractmethod

class DatasetFormat(ABC):
    def __init__(self, load_path, save_path):
        self.load_path = load_path
        self.save_path = save_path

    def convert_load_path_to_save_path(self, path):
        if path.startswith(self.load_path):
            return os.path.join(self.save_path, path[len(self.load_path) + 1:])
        else:
            raise ValueError(f'Expected "{path}" to start with "{self.load_path}"')

    @abstractmethod
    def get_scene_paths(self):
        raise NotImplementedError()

class ProbaVFormat(DatasetFormat):
    def __init__(self, load_path, save_path):
        super().__init__(load_path=load_path, save_path=save_path)

    def __get_train_scene_paths(self):
        return glob.glob(os.path.join(self.load_path, 'train', 'RED', 'imgset*')) +\
            glob.glob(os.path.join(self.load_path, 'train', 'NIR', 'imgset*'))

    def __get_test_scene_paths(self):
        return glob.glob(os.path.join(self.load_path, 'test', 'RED', 'imgset*')) +\
            glob.glob(os.path.join(self.load_path, 'test', 'NIR', 'imgset*'))

    def get_scene_paths(self, test=False):
        if test: return self.__get_test_scene_paths()
        else: return self.__get_train_scene_paths()
