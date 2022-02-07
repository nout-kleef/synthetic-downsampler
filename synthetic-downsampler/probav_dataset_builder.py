from synthetic_dataset_builder import SyntheticDatasetBuilder

class ProbaVDatasetBuilder(SyntheticDatasetBuilder):
    def __init__(self, args):
        super().__init__(args=args)

    def produce_lowres(self):
        pass
