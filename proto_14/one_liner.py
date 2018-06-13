#!/usr/bin/env python3

import os

CONVERT_NUM_TP = ("0.75", "1.25")


if __name__ == "__main__":
    cur_dir = os.getcwd()
    fnms = os.listdir(cur_dir)
    old_paths = [a_path for a_path in fnms
                 if os.path.splitext(a_path)[1] == ".csv"]
    z_dis_li = []
    nm_vas_li = []
    for csv_path in old_paths:
        fbase, ext = os.path.splitext(csv_path)
        nm_vas = fbase.split("_")
        z_dis = nm_vas[-1]
        z_dis_li.append(z_dis)
        nm_vas_li.append(nm_vas)
    z_dis_li = list(set(z_dis_li))
    z_dis_li.sort(key=float, reverse=True)
    convert_dict = dict(list(zip(z_dis_li, CONVERT_NUM_TP)))
    new_paths = []
    for nm_vas in nm_vas_li:
        tmp_key = nm_vas[-1]
        nm_vas[-1] = convert_dict[tmp_key]
        new_path = "_".join(nm_vas)
        new_path += ".csv"
        new_paths.append(new_path)
    for old, new in zip(old_paths, new_paths):
        os.rename(old, new)
