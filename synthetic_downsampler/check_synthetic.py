import filecmp
import glob
import os
import argparse

def is_authentic_lr(auth_lr, lr):
    # ensure LRx.png == LRx.png
    auth_lr_suffix = auth_lr[auth_lr.index('LR'):]
    lr_suffix = lr[lr.index('LR'):]
    if auth_lr_suffix != lr_suffix:
        raise ValueError(f'Names {auth_lr} and {lr} don\'t match')
    return filecmp.cmp(auth_lr, lr, shallow=False)

def is_synthetic_scene(auth_scene, scene):
    # ensure imgsety == imgsety
    auth_scene_suffix = auth_scene[auth_scene.index('imgset'):]
    scene_suffix = scene[scene.index('imgset'):]
    if auth_scene_suffix != scene_suffix:
        raise ValueError(f'Names {auth_scene} and {scene} don\'t match')
    auth_lrs = sorted(glob.glob(os.path.join(auth_scene, 'LR*.png')))
    lrs = sorted(glob.glob(os.path.join(scene, 'LR*.png')))
    if len(auth_lrs) != len(lrs):
        raise ValueError(f'{auth_scene} LR count does not match {scene}')
    num_auth = 0
    for auth_lr, lr in zip(auth_lrs, lrs):
        if is_authentic_lr(auth_lr, lr):
            num_auth += 1
    assert num_auth == 0 or num_auth == len(lrs), f'{num_auth} LRs out of {len(lrs)} were authentic'
    return num_auth == 0

def get_synth_auth_scene_counts(auth_root, root):
    """
    return: {
        "synth": int = number of synthetic scenes
        "auth": int = number of authentic scenes
    }
    """
    result = {
        "synth": 0,
        "auth": 0
    }
    auth_scenes = sorted(glob.glob(os.path.join(auth_root, '*', 'imgset*')))
    scenes = sorted(glob.glob(os.path.join(root, '*', 'imgset*')))
    if len(auth_scenes) != len(scenes):
        raise ValueError(f'{auth_root} scene count ({len(auth_scenes)}) does not match {root} ({len(scenes)})')
    for auth_scene, scene in zip(auth_scenes, scenes):
        if is_synthetic_scene(auth_scene, scene):
            result['synth'] += 1
        else:
            result['auth'] += 1
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Verify whether a directory contains the desired mix of authentic/synthetic data')
    parser.add_argument('auth_dataset', help='Root of dataset that is known to contain *only* authentic data')
    parser.add_argument('dataset', help='Root of dataset that is to be tested')
    parser.add_argument('part_synth', choices=['synth100', 'synth50'], default='synth100')
    args = parser.parse_args()

    auth_train = os.path.join(args.auth_dataset, 'train')
    auth_val = os.path.join(args.auth_dataset, 'val')
    train = os.path.join(args.dataset, 'train')
    val = os.path.join(args.dataset, 'val')

    # verify training data
    if args.part_synth == 'synth100':
        train_counts = get_synth_auth_scene_counts(auth_root=auth_train, root=train)
        assert train_counts['auth'] == 0, f'Found {train_counts["auth"]} authentic scenes, expected 0'
        assert train_counts['synth'] > 100, f'Found only {train_counts["synth"]} synthetic scenes'
    elif args.part_synth == 'synth50':
        train_counts = get_synth_auth_scene_counts(auth_root=auth_train, root=train)
        assert train_counts['auth'] > 50, f'Found only {train_counts["auth"]} authentic scenes'
        assert train_counts['synth'] > 50, f'Found only {train_counts["synth"]} synthetic scenes'
        assert abs(train_counts['auth'] - train_counts['synth']) <= 1, f'Scenes: {train_counts["auth"]} vs {train_counts["synth"]}'
    # verify that validation set is authentic
    val_counts = get_synth_auth_scene_counts(auth_root=auth_val, root=val)
    assert val_counts['synth'] == 0, f'Found {val_counts["synth"]} synthetic scenes, expected 0'
    assert val_counts['auth'] > 100, f'Found only {val_counts["auth"]} authentic scenes'
    print('SUCCESS!')
