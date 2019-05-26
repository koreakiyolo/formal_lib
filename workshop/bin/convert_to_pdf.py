#!/usr.bine/env python3

# formal lib
import os
# my lib
from convert_to_pdf import ConverterToPdf
from help_argparse import fnmstr
from help_argparse import dirstr
from help_argparse import print_global_varibales


if __name__ == "__main__":
    import argparse
    msg = "this program convert pngs to pdf."
    parser = argparse.ArgumentParser(
                                description=msg,
                                fromfile_prefix_chars="@")
    parser.add_argument("png_files", type=fnmstr, nargs="*")
    parser.add_argument("--png_dir", type=dirstr, nargs="?", default=None)
    parser.add_argument("--out_pdf", type=str, nargs="?",
                        requried=True)
    args = parser.parse_args()
    PNG_FILES = args.png_files
    PNG_DIR = args.png_dir
    OUT_PDF = args.out_pdf
    print_global_varibales(globals())
    converter_ins = ConverterToPdf()
    if PNG_DIR is not None:
        converter_ins.add_png_from_dir(
                                    PNG_DIR)
    else:
        converter_ins.add_png(PNG_FILES)
    converter_ins.

