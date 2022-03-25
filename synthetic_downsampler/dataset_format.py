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
    def get_train_scene_paths(self):
        raise NotImplementedError()

    @abstractmethod
    def get_eval_scene_paths(self):
        raise NotImplementedError()

class ProbaVFormat(DatasetFormat):
    def __init__(self, load_path, save_path):
        super().__init__(load_path=load_path, save_path=save_path)

    def _get_scene_paths(self, split, imgkind):
        return glob.glob(os.path.join(self.load_path, split, imgkind, 'imgset*'))

    def get_train_scene_paths(self):
        return self._get_scene_paths('train', 'RED') + self._get_scene_paths('train', 'NIR')

    def get_eval_scene_paths(self):
        return self._get_scene_paths('val', 'RED') + self._get_scene_paths('val', 'NIR')
