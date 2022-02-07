import argparse
import synthetic_dataset_builder, probav_dataset_builder


def main():
    parser = argparse.ArgumentParser(description='Create a synthetic dataset from high-resolution ground truth.')
    parser.add_argument('load_path', help='Path to root directory containing HR images')
    parser.add_argument('save_path', help='Path to root of directory where to store produced LR images')
    parser.add_argument('--format', choices=['probav'], default='probav')
    parser.add_argument('--random_seed', help='Random seed to make results reproducible')
    args = parser.parse_args()
    # produce a new dataset
    if args.format == 'probav':
        dataset = probav_dataset_builder.ProbaVDatasetBuilder(args)
    dataset.produce_dataset()

if __name__ == '__main__':
    main()
