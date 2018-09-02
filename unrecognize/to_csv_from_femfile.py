#!/usr/bin/env python3

# mylib
import os
# formal lib
from parser_fem import AdminFemFile


if __name__ == "__main__":
    import argparse
    msg = "this program convert a fem input file to three csv."
    parser = argparse.ArgumentParser(msg,
                                     fromfile_prefix_chars="@")
    parser.add_argument("input_file")
    parser.add_argument("--output_dir", default=None, type=str)
    args = parser.parse_args()
    INPUT_FILE = args.input_file
    OUTPUT_DIR = args.output_dir
    OUTPUT_FILES = ["c2.csv", "c3.csv", "c4.csv"]
    if OUTPUT_DIR is not None:
        OUTPUT_FILES = [os.path.join(OUTPUT_DIR, fnm)
                        for fnm in OUTPUT_FILES]
    # main part in the following
    AdminFemFile(INPUT_FILE)
    AdminFemFile.set_total_dfs()
    AdminFemFile.to_save_csv(OUTPUT_FILES)
