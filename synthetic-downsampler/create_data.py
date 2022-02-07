import argparse
from synthetic_dataset import SyntheticDataset


def main():
    parser = argparse.ArgumentParser(description='Create a synthetic dataset from high-resolution ground truth.')
    parser.add_argument('load_path', help='Path to root directory containing HR images')
    parser.add_argument('save_path', help='Path to root of directory where to store produced LR images')
    args = parser.parse_args()
    # produce a new dataset
    dataset = SyntheticDataset(load_path=args.load_path, save_path=args.save_path)
    dataset.produce_lowres()

if __name__ == '__main__':
    main()
