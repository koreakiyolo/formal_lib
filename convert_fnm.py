#!/usr/bin/env python3


import os


def convert_fnm(b_fnm, write_dir=None):
    if not os.path.exists(b_fnm):
        raise OSError
    p_dir, target_fnm = os.path.split(b_fnm)
    a_fnm = target_fnm.replace(" ", "_")
    if write_dir is None:
        new_path = os.path.join(p_dir, a_fnm)
    else:
        new_path = os.path.join(write_dir, a_fnm)
    os.rename(b_fnm, new_path)


def search_fnm(a_dir):
    fnms = os.listdir(a_dir)
    fnms = (fnm for fnm in fnms if " " in fnm)
    paths = [os.path.join(a_dir, fnm) for
             fnm in fnms]
    return paths


def main_func(a_dir, write_dir):
    paths = search_fnm(a_dir)
    [convert_fnm(a_path, write_dir) for a_path in paths]


if __name__ == "__main__":
    import argparse
    msg = "this program convert file names which includes 'space' in target "\
          "dir. it returns file names without 'space'"
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument("target_dirs", nargs="*", type=str)
    parser.add_argument("--write_dir", nargs="?", type=str, default=None)
    args = parser.parse_args()
    TARGET_DIRS = args.target_dirs
    WRITE_DIR = args.write_dir
    TARGET_DIRS = [a_path for a_path in TARGET_DIRS
                   if os.path.isdir(a_path)]
    if len(TARGET_DIRS) == 0:
        raise AssertionError
    for a_dir in TARGET_DIRS:
        main_func(a_dir, WRITE_DIR)
