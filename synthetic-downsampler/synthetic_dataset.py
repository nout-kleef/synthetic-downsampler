class SyntheticDataset(object):
    def __init__(self, load_path, save_path):
        self.load_path = load_path
        self.save_path = save_path

    def produce_lowres(self):
        pass

    @staticmethod
    def _produce_lowres_for_scene():
        pass
