import filecmp
import glob
import os

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
