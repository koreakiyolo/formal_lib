#!/usr/bin/env python3
# !coding:utf-8

import pandas as pd
import os
from io import StringIO

def remove_cmt_line(txt_line, com_mark="#"):
    spnum = txt_line.find(com_mark)
    if spnum == -1:
        return txt_line
    else:
        new_txtline = txt_line[:spnum] + "\n"
        return new_txtline


def load_csv_modified(fnm):
    with open(fnm, "r") as read:
        remove_cmt = [remove_cmt_line(one_line)
                      for one_line in read]
    f = StringIO()
    f.writelines(remove_cmt)
    f.seek(0)
    ans_df = pd.read_csv(f, header=None, delim_whitespace=True)
    return ans_df


def set_column_from_fnm(col_txt, target_df):
    with open(col_txt, "r") as read:
        columns = [one_line.strip() for one_line in read]
    target_df.columns = columns
    return target_df


def convert_ext(fnm, ext="csv"):
    tmp = os.path.splitext(fnm)
    new_path = tmp[0] + "." + ext
    return new_path


if __name__ == "__main__":
    import argparse
    msg = ""
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument("--col_fnm", type=str, nargs="?", required=True)
    parser.add_argument("target_ftxts", nargs="*", type=str)
    parser.add_argument("--write_dir", nargs="?", type=str, required=True)
    args = parser.parse_args()
    TARGET_FTXTS = args.target_ftxts
    COL_FNM = args.col_fnm
    WRITE_DIR = args.write_dir
    if not os.path.exists(COL_FNM):
        raise OSError
    for t_fnm in TARGET_FTXTS:
        if not os.path.exists(t_fnm):
            raise OSError
        ans_df = load_csv_modified(t_fnm)
        set_column_from_fnm(COL_FNM, ans_df)
        new_path = convert_ext(t_fnm)
        tmp = os.path.split(new_path)[1]
        wpath = os.path.join(WRITE_DIR, tmp)
        ans_df.to_csv(wpath)
    print("completed")
