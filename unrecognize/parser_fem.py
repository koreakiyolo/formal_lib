#!/usr/bin/env python3


import numpy as np
import pandas as pd
import tempfile
from itertools import islice

# == global varibale part ==
# 2C part colnms
POINT_COL = "point_id"
ELM_X_COL = "x_pos"
ELM_Y_COL = "y_pos"
ELM_Z_COL = "z_pos"
C2_PART_COLS = [POINT_COL, ELM_X_COL,
                ELM_Y_COL, ELM_Z_COL]
# 3C part colnms
ELM_COL = "elm_id"
POINT_COLBASE = "point_"
# 4C part colnms
TSTEP_COL = "time_step"
POINT_ID_COL = "point_id"
PROPERTY_COL = "property"


def get_component_num(read_iter, kword="2C"):
    for line in read_iter:
        ini_va, compo_num = line.split()[0:2]
        if ini_va == kword:
            return int(compo_num)
    else:
        raise AssertionError("invalid type file")


def load_C2_part_from_read(read_iter, point_num,
                           confirm=True):
    C2_part_iter = islice(read_iter, point_num)
    tmp_fnm = tempfile.NamedTemporaryFile(mode="wb")
    for line in C2_part_iter:
        tmp_fnm.write(line)
    tmp_fnm.flush()
    tmp_fnm.seek(0)
    df_pointid_and_pos = pd.read_csv(tmp_fnm,
                                     header=None,
                                     sep="\s+",
                                     nrows=point_num)
    if confirm:
        assert_cond = df_pointid_and_pos[0] == -1
        if np.count_nonzero(~assert_cond) != 0:
            raise AssertionError("invalid type in 2C part")
    reduced_df = df_pointid_and_pos.iloc[:, [1, 2, 3, 4]]
    reduced_df.columns = C2_PART_COLS
    df_pointid_and_pos = reduced_df.set_index(POINT_COL)
    return df_pointid_and_pos


def load_C3_part_from_read(read_iter, elm_num):
    C3_part_iter = islice(read_iter, elm_num*2)
    point_ids = []
    tmp_fob = tempfile.NamedTemporaryFile(mode="wb")
    for line in C3_part_iter:
        lvals = line.split()
        if lvals[0] == "-1":
            point_ids.append(int(lvals[1]))
        if lvals[0] == "-2":
            tmp_fob.write(",".join(lvals[1:]) + "\n")
    tmp_fob.flush()
    tmp_fob.seek(0)
    df_elmid_and_elm = pd.read_csv(tmp_fob,
                                   header=None,
                                   index=point_ids)
    _, colnum = df_elmid_and_elm.size
    new_colnms = _make_C3_df_colnms(colnum)
    df_elmid_and_elm.columns = new_colnms
    return df_elmid_and_elm


def _make_C3_df_colnms(col_size):
    colnms = [POINT_COLBASE + str(i) for i in col_size]
    return colnms


def load_C4_part_from_read(read_gene, point_num):
    tmp_fob = tempfile.NamedTemporaryFile(mode="wb")
    for line in read_gene:
        lvals = line.split()
        if lvals[0] == "-1":
            tmp_fob.write(",".join(lvals[1:]) + "\n")
    tmp_fob.flush()
    tmp_fob.seek(0)
    point_and_prop_df = pd.read_csv(tmp_fob, header=None,
                                    columns=[POINT_ID_COL, PROPERTY_COL])
    total_num = len(point_and_prop_df)
    tstep_ar = _make_tstep_ar(total_num, point_num)
    point_and_prop_df[TSTEP_COL] = tstep_ar
    return point_and_prop_df


def _make_tstep_ar(total_num, point_num):
    tstep_num = total_num / point_num
    if type(tstep_num) == float:
        raise AssertionError
    stack_li = [np.arange(1, tstep_num+1)] * point_num
    mat_tnum_pnum = np.vstack(stack_li).T
    tstep_ar = mat_tnum_pnum.flatten()
    return tstep_ar.astype(np.int64)


class AdminFemFile(object):
    def __init__(self, fpath):
        read = open(fpath, "r")
        self.read_iter = read

    def set_total_dfs(self):
        self.point_num = get_component_num(self.read_iter, "2C")
        self.df_pointid_and_pos = load_C2_part_from_read(self.read_iter,
                                                         self.point_num)
        self.elm_num = get_component_num(self.read_iter, "3C")
        self.df_elmid_and_elm = load_C3_part_from_read(self.read_iter,
                                                       self.elm_num)
        self.df_pid_tstep_property = load_C4_part_from_read(self.read_iter,
                                                            self.point_num)

    def to_save_csv(self, save_csvs):
        if len(save_csvs) != 3:
            raise IndexError
        c2_csv, c3_csv, c4_csv = save_csvs
        self.df_pointid_and_pos.to_csv(c2_csv)
        self.df_elmid_and_elm.to_csv(c3_csv)
        self.df_pid_tstep_property.to_csv(c4_csv)
