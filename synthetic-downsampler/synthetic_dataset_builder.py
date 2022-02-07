from abc import ABC, abstractmethod

class SyntheticDatasetBuilder(ABC):
    def __init__(self, args):
        self.load_path = args.load_path
        self.save_path = args.save_path
        self.random_seed = args.random_seed

    @abstractmethod
    def produce_lowres(self):
        raise NotImplementedError()

    @staticmethod
    def _produce_lowres_for_scene():
        pass
