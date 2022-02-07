class SyntheticDataset(object):
    def __init__(self, args):
        self.load_path = args.load_path
        self.save_path = args.save_path
        self.random_seed = args.random_seed

    def produce_lowres(self):
        pass

    @staticmethod
    def _produce_lowres_for_scene():
        pass
