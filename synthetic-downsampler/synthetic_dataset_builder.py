class SyntheticDatasetBuilder(object):
    def __init__(self, args):
        self.load_path = args.load_path
        self.save_path = args.save_path
        self.random_seed = args.random_seed
        self.format = None

    def produce_lowres(self):
        scenes = self.format.get_scene_paths()
        print(f'Producing synthetic low resolution data for {len(scenes)} scenes')
        for scene in scenes:
            self._produce_lowres_for_scene(scene)

    def _produce_lowres_for_scene(self, scene):
        save_dir = self.format.convert_load_path_to_save_path(scene)
        pass
