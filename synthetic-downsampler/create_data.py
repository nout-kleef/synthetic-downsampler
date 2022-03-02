import argparse
import synthetic_dataset_builder
from downsampler import BicubicDownsampler


def main():
    parser = argparse.ArgumentParser(description='Create a synthetic dataset from high-resolution ground truth.')
    parser.add_argument('load_path', help='Path to root directory containing HR images')
    parser.add_argument('save_path', help='Path to root of directory where to store produced LR images')
    parser.add_argument('--eval_dir', choices=['val', 'test'], default='val')
    parser.add_argument('--skip_if_exists', action='store_true')
    parser.add_argument('--format', choices=['probav'], default='probav')
    parser.add_argument('--random_seed', help='Random seed to make results reproducible')
    args = parser.parse_args()
    # produce a new dataset
    downsampler = BicubicDownsampler(factor=3)
    if args.format == 'probav':
        dataset = synthetic_dataset_builder.ProbaVDatasetBuilder(args, downsampler)
    dataset.produce_dataset()

if __name__ == '__main__':
    main()
