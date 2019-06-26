#!/usr/bin/env python3

# formal lib
import os
# my lib
from change_png_to_pdf import ConverterToPdf


def print_global_varibales():
    glva_dict = globals()
    print_dict = {key: va for key, va in glva_dict
                  if key.isupper()}
    print("== global varibale is in the following. ==")
    print(print_dict)
    print("==========================================")


def fnmstr(path_str):
    if not os.path.exists(path_str):
        mes = "{} is not file.".format(
                                    path_str
                                      )
        raise OSError(mes)
    return path_str


def dirstr(path_str):
    if not os.path.isdir(path_str):
        mes = "{} is not directory.".format(
                                        path_str
                                           )
        raise OSError(mes)
    return path_str


if __name__ == "__main__":
    import argparse
    msg = "this program convert pngs to pdf."
    parser = argparse.ArgumentParser(
                                description=msg,
                                fromfile_prefix_chars="@")
    parser.add_argument("png_files", type=fnmstr, nargs="*")
    parser.add_argument("--png_dir", type=dirstr, nargs="?", default=None)
    parser.add_argument("--out_pdf", type=str, nargs="?",
                        required=True)
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
    converter_ins.to_pdf(OUT_PDF)
