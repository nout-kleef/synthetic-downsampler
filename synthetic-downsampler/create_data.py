import argparse
import os
import synthetic_dataset_builder
from downsampler import BicubicDownsampler

def main():
    parser = argparse.ArgumentParser(description='Create a synthetic dataset from high-resolution ground truth.')
    parser.add_argument('load_path', help='Path to root directory containing HR images')
    parser.add_argument('save_path', help='Path to root of directory where to store produced LR images')
    parser.add_argument('noise1_sigma', type=float)
    parser.add_argument('degrade1_sigma', type=float)
    parser.add_argument('noise2_sigma', type=float)
    parser.add_argument('part_auth', choices=['auth0', 'auth100', 'auth50'], default='auth0')
    parser.add_argument('part_synth', choices=['synth100', 'synth50'], default='synth100')
    parser.add_argument('--eval_dir', choices=['val', 'test'], default='val')
    parser.add_argument('--skip_if_exists', action='store_true')
    parser.add_argument('--format', choices=['probav'], default='probav')
    args = parser.parse_args()
    create_dataset(
        [
            (BicubicDownsampler._noise,             {'sigma': args.noise1_sigma}),
            (BicubicDownsampler._degrade,           {'sigma': args.degrade1_sigma}),
            (BicubicDownsampler._direct_downsample, {'factor': 3}),
            (BicubicDownsampler._noise,             {'sigma': args.noise2_sigma}),
        ],
        args.format,
        args.load_path,
        args.save_path,
        args.eval_dir,
        args.skip_if_exists,
        args.part_auth,
        args.part_synth
    )
    

def create_dataset(pipeline, format, load_path, save_path, eval_dir, skip_if_exists, part_auth, part_synth):
    os.makedirs(save_path, exist_ok=True)
    downsampler = BicubicDownsampler(pipeline, save_path)
    if format == 'probav':
        if part_auth == 'auth0' and part_synth == 'synth100':
            dataset = synthetic_dataset_builder.ProbaVDatasetBuilder(
                downsampler, load_path, save_path, eval_dir, skip_if_exists
            )
        elif part_auth == 'auth100' and part_synth == 'synth100':
            dataset = synthetic_dataset_builder.ProbaVDatasetBuilder100_100(
                downsampler, load_path, save_path, eval_dir, skip_if_exists
            )
        elif part_auth == 'auth50' and part_synth == 'synth50':
            dataset = synthetic_dataset_builder.ProbaVDatasetBuilder50_50(
                downsampler, load_path, save_path, eval_dir, skip_if_exists
            )
        else:
            raise ValueError(f'Unexpected data mix: {part_auth}/{part_synth}')
    else:
        raise ValueError(f'Unknown format {format}')
    dataset.produce_dataset()

if __name__ == '__main__':
    main()
