from synthetic_dataset_builder import SyntheticDatasetBuilder
from dataset_format import ProbaVFormat

class ProbaVDatasetBuilder(SyntheticDatasetBuilder):
    def __init__(self, args, downsampler):
        super().__init__(args=args, downsampler=downsampler)
        self.format = ProbaVFormat(load_path=args.load_path, save_path=args.save_path)
