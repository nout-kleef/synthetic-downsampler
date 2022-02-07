from synthetic_dataset_builder import SyntheticDatasetBuilder
from dataset_format import ProbaVFormat

class ProbaVDatasetBuilder(SyntheticDatasetBuilder):
    def __init__(self, args):
        super().__init__(args=args)
        self.format = ProbaVFormat(args.load_path)
