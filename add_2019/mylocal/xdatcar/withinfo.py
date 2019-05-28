#!/usr/bin/env python
# !coding:utf-8

import numpy as np
import sys
from pandas import DataFrame
import pandas as pd

# my library
from core import Xdatcar
from layer import GetLayersOfAxis


if "2.7" in sys.version:
    input = raw_input


class XdatWithInfo(Xdatcar):
    def __init__(self, xdat_data, especial_info_ar,
                 especial_step_li=None, layers_li=None,
                 tolerance=1.0e-5):
        super(Xdatcar, self).__init__(xdat_data)
        self.switch_main_data()
        self.especial_info_ar = especial_info_ar
        self.especial_step_li = especial_step_li
        if layers_li is None:
            self.divide_pos_to_layers(tolerance)
        if type(especial_step_li) is list:
            gene_step = self.gene_extract_step(especial_step_li)
            stack_fgene = (self.fracvecs[ini:fin] for ini, fin in gene_step)
            self.especial_fposvecs = np.vstack(stack_fgene)
            gene_step = self.gene_extract_step(especial_step_li)
            stack_cgene = (self.cartvecs[ini:fin] for ini, fin in gene_step)
            self.especial_cposvecs = np.vstack(stack_cgene)
        elif especial_step_li is None:
            self.especial_fposvecs = self.fracvecs
            self.especial_cposvecs = self.cartvecs
        else:
            sys.stderr.write("especial_step_li must be list.\n")
            sys.exit(2)

    def divide_pos_to_layers(self, tolerance=1.0e-2):
        getlay_ins = GetLayersOfAxis(self._get_each_step(0), self.latvecs)
        self.layers_li = getlay_ins.get_layers_li()

    def gene_extract_step(self, step_li):
        for step in step_li:
            init = step * self.total_at
            fin = init + self.total_at
            yield (init, fin)

    def to_cnvt_step_info(self):
        step_ins = StepInfo()
        step_ins.load_from_args(self.especial_fposvecs,
                                self.especial_cposvecs,
                                self.especial_info_ar,
                                self.total_at,
                                self.especial_step_li)
        return step_ins


class StepInfo(object):
    def __init__(self):
        fpos_vecs = None
        cpos_vecs = None
        especial_info_ar = None
        total_at = None
        especial_step_li = None

    def load_from_args(self, fpos_vecs, cpos_vecs,
                       especial_info_ar, total_at,
                       especial_step_li=None, confirm=True):
        self.fpos_vecs = fpos_vecs
        self.cpos_vecs = cpos_vecs
        self.total_at = total_at
        self.especial_info_ar = especial_info_ar
        if especial_step_li is None:
            total_step = len(self.fpos_vecs) / self.total_at
            self.especial_step_li = range(total_step)
        num = len(self.fpos_vecs)
        self.especial_info_ar = self.especial_info_ar.reshape(num, -1)
        self.especial_info_ar = self.especial_info_ar.astype(np.int64)
        self.atom_id_gene = (np.arange(total_at) for
                             i in self.especial_step_li)
        self.step_id_gene = self._make_gene_step_ar()
        if confirm:
            self.confirm_input_data()

    def load_from_csv(self, fcsv, atom_num=None, confirm=True):
        self.total_csv = pd.read_csv(fcsv)
        tmp = self.total_csv[:, ["fpos_x", "fpos_y", "fpos_z"]]
        self.fpos_vecs = tmp.values
        tmp = self.total_csv[:, ["cpos_x", "cpos_y", "cpos_z"]]
        self.cpos_vecs = tmp.values
        columns = [nm for nm in self.total_csv.columns
                   if "info" in nm]
        self.especial_info_ar = self.total_csv[columns].values
        tmp = self.total_csv["step_id"].values
        self.especial_step_li = np.unique(tmp)
        if atom_num is None:
            self.total_at = int(input("what is atom number?:"))
        self.atom_id_gene = (np.arange(self.total_at) for
                             i in self.especial_step_li)
        self.step_id_gene = self._make_gene_step_ar()
        if confirm:
            self.confirm_input_data()

    def get_df(self, info_names=None):
        tmp_ar = np.hstack((self.fpos_vecs,
                            self.cpos_vecs,
                            self.especial_info_ar))
        frac_names = ["fpos_x", "fpos_y", "fpos_z"]
        cart_names = ["cpos_x", "cpos_y", "cpos_z"]
        if info_names is None:
            num = self.especial_info_ar.shape[1]
            info_names = ["info_" + str(i) for i in range(num)]
        column_names = frac_names + cart_names + info_names
        total_df = DataFrame(tmp_ar, columns=column_names)
        atom_idars = np.hstack(self.atom_id_gene)
        step_idars = np.hstack(self.step_id_gene)
        total_df["atom_id"] = atom_idars
        total_df["step_id"] = step_idars
        return total_df

    def set_df(self, clear=True, info_names=None):
        self.total_df = self.get_df(info_names)
        if clear:
            self.clear_data()

    def to_csv(self, wpath):
        self.total_df.to_csv(wpath)

    def _make_gene_step_ar(self):
        for step in self.especial_step_li:
            yield np.array([step] * self.total_at)

    def confirm_input_data(self):
        fpos_len = len(self.fpos_vecs)
        cpos_len = len(self.cpos_vecs)
        info_len = len(self.especial_info_ar)
        step_len = len(self.especial_step_li)
        print(info_len, fpos_len, cpos_len)
        if not (fpos_len == cpos_len and fpos_len == info_len):
            raise TypeError("data lengths unmatch. in "
                            "StepInfoSeq instance.")
        if step_len != fpos_len / self.total_at:
            raise TypeError("expected step lengths unmatch. in "
                            "StepInfoSeq instance")

    def clear_data(self):
        self.fpos_vecs = None
        self.fpos_vecs = None
        self.cpos_vecs = None
        self.especial_info_ar = None
        self.total_at = None
        self.especial_step_li = None

    def add_layers_info(self, layer_ids_li):
        atom_idar = self.total_df["atom_id"].values
        total_length = len(self.total_df)
        ans_ar = np.zeros(total_length)
        for lay_num, layer_ids in enumerate(layer_ids_li):
            cond_li = []
            for a_id in layer_ids:
                cond = atom_idar == a_id
                cond_li.append(cond)
            tmp = np.vstack(cond_li)
            a_layer_cond = np.max(tmp, axis=0)
            ans_ar[a_layer_cond] = lay_num
        self.total_df["layer_id"] = ans_ar.astype(np.int64)
