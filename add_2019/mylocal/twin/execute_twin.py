#!/usr/bin/env python
# !coding:utf-8

# formal library
import os
import sys
# my library
from make_twin import PosTwin

if __name__ == "__main__":
    import argparse
    ms = "this program is useful for making twin model structure "\
         "including grainboundary. however, it can apply to only "\
         "hexagonal."
    parser = argparse.ArgumentParser(description=ms, fromfile_prefix_chars="@")
    parser.add_argument("--poscar_path", args="?",
                        type=str, required=True)
    parser.add_argument("--twininfo_path", args="?",
                        type=str, required=True)
    parser.add_argument("--output_dir", args="?",
                        type=str, default="./")
    args = parser.parse_args()
    pospath = args.poscar_path
    twinpath = args.twininfo_path
    output_dir = args.output_dir
    if not (os.path.exists(pospath) and
            os.path.exists(twinpath)):
        sys.stderr.write("(1)poscar and (2)twin info path "
                         "don't existi.\n")
        sys.exit(2)
    if os.path.isdir(output_dir):
        pass
    elif os.path.exists(output_dir):
        sys.stderr.write("path of output_dir you "
                         "entered has already existed.\n"
                         "such path isn't directory.\n")
        sys.exit(2)
    else:
        while True:
            tmp = raw_input("make directory into " + output_dir + " ?:(y/n)")
            if tmp == "y" or tmp == "n":
                break
        if tmp == "y":
            os.path.mkdirs(output_dir)
        else:
            sys.stderr.write("program is paused.\n")
            sys.exit(2)
    twinpos_ins = PosTwin(pospath, twinpath)
    twinpos_ins.to_one_side_spcell()
    gene_notb = twinpos_ins.gene_translated_matrixfpos(False)
    gene_onb = twinpos_ins.gene_translated_matrixfpos(True)
    next(gene_notb)
    notb_path = os.path.join(output_dir, "POSCAR_noton_boundary")
    twinpos_ins.write_to_poscar(notb_path)
    next(gene_onb)
    onb_path = os.path.join(output_dir, "POSCAR_on_boudary")
    twinpos_ins.write_to_poscar(onb_path)
