import glob
import os
from pathlib import Path
import shutil
import tqdm
from dataset_format import ProbaVFormat

class SyntheticDatasetBuilder(object):
    def __init__(self, args, format, downsampler):
        self.load_path = args.load_path
        self.save_path = args.save_path
        self.random_seed = args.random_seed
        self.eval_dir = args.eval_dir
        self.format = format
        self.downsampler = downsampler

    def produce_dataset(self):
        self._produce_training_data()
        self._produce_eval_data()

    def _produce_training_data(self, skip_if_exists=True):
        auth_scenes = self.format.get_train_scene_paths()
        print(f'Producing synthetic low resolution data for {len(auth_scenes)} scenes')
        if skip_if_exists and os.path.exists(os.path.join(self.save_path, 'train')):
            print(f'WARN: training data directory already exists. Skipping step.')
            return
        total_lrs = 0
        for auth_scene in tqdm.tqdm(auth_scenes):
            synth_scene, num_lrs = self._produce_synthetic_scene(auth_scene)
            self._produce_lowres_images(synth_scene, num_lrs)
            total_lrs += num_lrs
        print(f'Produced {total_lrs} low-resolution images (avg {total_lrs / len(auth_scenes):.1f} per scene)')

    def _produce_eval_data(self, skip_if_exists=True):
        auth_scenes = self.format.get_eval_scene_paths()
        print(f'Copying evaluation data for {len(auth_scenes)} scenes to synthetic dataset')
        if skip_if_exists and os.path.exists(os.path.join(self.save_path, self.eval_dir)):
            print(f'WARN: evaluation data directory already exists. Skipping step.')
            return
        for auth_scene in tqdm.tqdm(auth_scenes):
            synth_scene = self.format.convert_load_path_to_save_path(auth_scene)
            shutil.copytree(auth_scene, synth_scene)
            
    def _produce_synthetic_scene(self, load_dir):
        save_dir = self.format.convert_load_path_to_save_path(load_dir)
        os.makedirs(save_dir, exist_ok=True)
        # copy HR + SM
        shutil.copy(Path(load_dir) / 'HR.png', save_dir)
        shutil.copy(Path(load_dir) / 'SM.png', save_dir)
        # produce LR images, copy quality maps
        lrs = glob.glob(os.path.join(load_dir, 'LR*.png'))
        for lr in lrs:
            lr = Path(lr)
            lr_idx = lr.name[2:-4]  # match /LR[0-9]+.png/
            quality_map_path = lr.parent / f'QM{lr_idx}.png'
            shutil.copy(quality_map_path, save_dir)
        return save_dir, len(lrs)

    def _produce_lowres_images(self, scene, num_lrs):
        self.downsampler.downsample(scene, num_lrs)

class ProbaVDatasetBuilder(SyntheticDatasetBuilder):
    def __init__(self, args, downsampler):
        super().__init__(
            args=args, 
            downsampler=downsampler,
            format=ProbaVFormat(load_path=args.load_path, save_path=args.save_path)
        )
