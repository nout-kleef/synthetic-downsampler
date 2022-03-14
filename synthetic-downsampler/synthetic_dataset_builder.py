import glob
import os
from pathlib import Path
import shutil
import tqdm
from dataset_format import ProbaVFormat

class SyntheticDatasetBuilder(object):
    def __init__(self, format, downsampler, load_path, save_path, eval_dir, skip_if_exists):
        self.format = format
        self.downsampler = downsampler
        self.load_path = load_path
        self.save_path = save_path
        self.eval_dir = eval_dir
        self.skip_if_exists = skip_if_exists

    def produce_dataset(self):
        self._produce_training_data()
        self._produce_eval_data()
        self._produce_metadata()

    def _produce_training_data(self):
        train_root = os.path.join(self.save_path, 'train')
        if os.path.exists(train_root):
            if self.skip_if_exists:
                print(f'WARN: {train_root} already exists. Skipping training data production step.')
                return
            else:
                print(f'WARN: {train_root} already exists. Purging existing data')
                shutil.rmtree(train_root)

    def _produce_synthetic_data(self, auth_scenes):
        print(f'Producing synthetic low resolution data for {len(auth_scenes)} scenes')
        total_lrs = 0
        for auth_scene in tqdm.tqdm(auth_scenes):
            synth_scene, num_lrs = self._produce_synthetic_scene(auth_scene)
            self._produce_lowres_images(synth_scene, num_lrs)
            total_lrs += num_lrs
        print(f'Produced {total_lrs} low-resolution images (avg {total_lrs / len(auth_scenes):.1f} per scene)')

    def _produce_eval_data(self):
        eval_root = os.path.join(self.save_path, self.eval_dir)
        if os.path.exists(eval_root):
            if self.skip_if_exists:
                print(f'WARN: {eval_root} already exists. Skipping eval data production step.')
                return
            else:
                print(f'WARN: {eval_root} already exists. Purging existing data')
                shutil.rmtree(eval_root)
        auth_scenes = self.format.get_eval_scene_paths()
        print(f'Copying evaluation data for {len(auth_scenes)} scenes to synthetic dataset')
        for auth_scene in tqdm.tqdm(auth_scenes):
            synth_scene = self.format.convert_load_path_to_save_path(auth_scene)
            shutil.copytree(auth_scene, synth_scene)

    def _produce_metadata(self):
        print('Copying metadata')
        norm_file = os.path.join(self.load_path, 'norm.csv')
        shutil.copy(norm_file, self.save_path)
            
    def _produce_synthetic_scene(self, load_dir):
        save_dir = self.format.convert_load_path_to_save_path(load_dir)
        os.makedirs(save_dir, exist_ok=True)
        # copy HR + SM + clearance.npy
        shutil.copy(Path(load_dir) / 'HR.png', save_dir)
        shutil.copy(Path(load_dir) / 'SM.png', save_dir)
        shutil.copy(Path(load_dir) / 'clearance.npy', save_dir)
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
    def __init__(self, downsampler, load_path, save_path, eval_dir, skip_if_exists):
        super().__init__(
            ProbaVFormat(load_path=load_path, save_path=save_path), 
            downsampler, 
            load_path, 
            save_path, 
            eval_dir, 
            skip_if_exists
        )

    def _get_scene_range(self, paths):
        min_scene = 1000000
        max_scene = -1
        for p in paths:
            num = int(p[-4:])
            min_scene = min(min_scene, num)
            max_scene = max(max_scene, num)
        return min_scene, max_scene + 1

    def _copy_authentic_scene(self, src_scene, dest_scene):
        if os.path.exists(dest_scene):
            raise ValueError(f'{dest_scene} already exists')
        shutil.copytree(src_scene, dest_scene)
        info_file = Path(dest_scene) / 'scene_info.txt'
        with open(info_file, 'w') as f:
            f.writelines(f'AUTHENTIC, origin: {src_scene}\n')

    def _copy_authentic_data(self, paths, offset):
        base_path = paths[0][:-4]
        for path in tqdm.tqdm(paths):
            scene_num = int(path[-4:])
            new_scene_num = scene_num + offset
            new_path = base_path + str(new_scene_num).zfill(4)
            new_path = self.format.convert_load_path_to_save_path(new_path)
            self._copy_authentic_scene(path, new_path)
            

    def _produce_training_data(self):
        SyntheticDatasetBuilder._produce_training_data(self)
        scenes = self.format.get_train_scene_paths()
        self._produce_synthetic_data(scenes)

class ProbaVDatasetBuilder100_100(ProbaVDatasetBuilder):
    def _produce_training_data(self):
        SyntheticDatasetBuilder._produce_training_data(self)
        # synthetic
        scenes = self.format.get_train_scene_paths()
        self._produce_synthetic_data(scenes)
        # authentic - copy over with appropriate offset
        self._copy_wrapper('NIR')
        self._copy_wrapper('RED')

    def _copy_wrapper(self, imgkind):
        scenes = self.format._get_scene_paths('train', imgkind)
        start_synth, end_synth = self._get_scene_range(scenes)
        num = end_synth - start_synth
        end_auth = num + num
        print(f'{imgkind}: {start_synth:>4} - {end_synth:>4}. synth:{start_synth:>4}-{end_synth - 1:>4}, auth:{num:>4}-{end_auth - 1:>4}')
        self._copy_authentic_data(scenes, offset=num)
