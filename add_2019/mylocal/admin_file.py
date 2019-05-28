#!/usr/bin/env python
# !:coding:utf-8

import os
import re
import glob
from collections.abc import Sequence
from collections import OrderedDict

class AdminFile(Sequence):
    def __init__(self):
        self.path_li = []

    def load_from_list(self, fpath_li):
        self.path_li.extend(fpath_li)

    def load_from_file(self, fpath_with_multipath):
        with open(fpath_with_multipath, "r") as read:
            self.path_li = [one_line.strip() for one_line in read]
        confirm_existing_path()

    def load_from_glob(self, glob_str):
        file_li = glob.glob(glob_str)
        self.path_li.extend(file_li)

    def write_to_file(self, wpath):
        write_li = [a_path + "\n" for a_path in self.path_li]
        with open(wpath, "w") as write:
            write.writelines(write_li)

    def add_file(self, fpath):
        if os.path.exists(fpath):
            self.path_li.append(fpath)
            confirm_existing_path()

    def remove_file(self, fpath):
        if fpath in self.path_li:
            self.path_li.remove(fpath)

    def restrict_filtype(self):
        tmp = [a_path for a_path in self.path_li
               if os.path.isfile(a_path)]
        self.path_li = tmp

    def restrict_dirtype(self):
        tmp = [a_path for a_path in self.path_li
               if os.path.isdir(a_path)]
        self.path_li = tmp

    def restrict_lntype(self):
        tmp = [a_path for a_path in self.path_li
               if os.path.islink(a_path)]
        self.path_li = tmp

    def add_dirtree(self, stem_dir, re_exp=r".*"):
        tmp_gene = self._gene_dirtree(stem_dir)
        tmp_gene = self._gene_reexpre_filered(tmp_gene, re_exp)
        tmp_li = list(tmp_gene)
        self.path_li.extend(tmp_li)

    def _gene_dirtree(self, stem_dir):
        for root, _, file_li in os.walk(stem_dir):
            yield root
            for a_file in file_li:
                yield os.path.join(root, a_file)

    def _gene_reexpre_filered(self, file_nm_li, re_exp):
        re_ins = re.compile(re_exp)
        for a_path in file_nm_li:
            ret_re = re_ins.match(a_path)
            if ret_re:
                yield a_path

    def cnvt_abspath(self, re_pre):
        tmp = [os.path.abspath(apath) for apath
               in self.path_li]
        self.path_li = tmp

    def confirm_existing_path(self):
        self.path_li = [apath for apath in self.path_li
                        if os.path.exists(apath)]

    def __iter__(self):
        for a_path in self.path_li:
            yield a_path

    def __getitem__(self, index):
        return self.path_li[index]

    def __len__(self):
        return len(self.path_li)


class FileGene(AdminFile):
    def __init__(self):
        super(FileGene, self).__init__()

    def __iter__(self):
        if len(self.path_li) == 0:
            raise StopIteration
        else:
            tmp = self.path_li.pop(0)
            yield tmp

class AdminParameterPairs(Sequence):
    def __init__(self, pair_num):
        self.pair_num = pair_num
        self.param_odict = OrderedDict()

    def load_from_li(self, paramobj_nargs*):
        if len(n_liargs) !=self.pair_num:
            raise TypeError("you must enter the same num of list"
                            " including paramobj_nargs.")
        else:
            for i, paramobj in enumerate(paramobj_nargs):
                self.paramobj_nargs[i] = paramobj

    def __iter__(self):
        for pairs_tp in zip(*self.file_li):
            yield pairs_tp

    def __len__(self):
        return self.pair_num
