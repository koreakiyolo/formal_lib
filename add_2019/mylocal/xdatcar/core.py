#!/usr/bin/env python
# !:coding:utf-8

import numpy as np
from numpy import linalg as la
import itertools as itrt
from collections import Sequence
import sys
import os


class XdatBase(Sequence):
    # it is container class adiministering xdatcar data of VASP.
    # it is a meta class. when using this, you must make another class
    # taking over it.
    
    def __init__(self, loaded_data=None):
        self.read_data(loaded_data)
        self.cartvecs = None
        self.main_data = self.fracvecs
        self.main_dtype = "fractional"

    def read_data(self, data):
        raise NotImplementedError

    def _set_cartvecs(self):
        self.cartvecs = np.dot(self.fracvecs, self.latvecs)

    def __getitem__(self, index):
        init = index * self.total_at
        fin = init + self.total_at
        return self.main_data[init:fin]

    def __len__(self):
        return self.total_step

    def __setitem__(self, index, va):
        init = index * self.total_at
        fin = init + self.total_at
        tmar = self.main_data[init:fin]
        if isinstance(va, np.ndarray):
            if tmar.shape == va.shape:
                self.main_data[init:fin] = va
            else:
                print("shape can't apply")
        else:
            print("need ndarray")

    def get_oneatom_data(self, atom_index):
        ref_data = range(atom_index, len(self.main_data), self.total_at)
        return self.main_data[ref_data]

    def _set_wlines(self):
        tmp_at = [str(va) for va in self.natm_li]
        at_line = " ".join(tmp_at) + "\n"
        elm_line = " ".join(self.elm_li) + "\n"
        self.elm_at_line = [elm_line, at_line]

    def write_xdatcar(self, wpath):
        self._set_wlines()
        with open(wpath, "w") as write:
            write.writelines(self.iniline)
            np.savetxt(write, self.latvecs)
            write.writelines(self.elm_at_line)
            for num in xrange(1, self.total_step + 1):
                write.write("Direct configulation=   "+str(num)+" \n")
                init = (num - 1) * self.total_at
                fin = init + self.total_at
                np.savetxt(write, self.fracvecs[init:fin])

    def write_step_to_poscar(self, step_num, wpath):
        if not isinstance(step_num, int):
            sys.stderr.write("step num must be int type.\n")
            sys.stderr.write("XdatBase.write_step_to_poscar is canceled.\n")
            sys.exit(2)
        ini_mes = str(step_num) + " step is extracted. \n"
        self._set_wlines()
        with open(wpath, "w") as write:
            write.write(ini_mes)
            write.write(str(1.0) + "\n")
            np.savetxt(write, self.latvecs)
            write.writelines(self.elm_at_line)
            write.writeline("Direct\n")
            tmp = self.main_data
            self.main_data = self.fracvecs
            one_step_fposvecs = self._get_each_step(step_num)
            np.savetxt(write, one_step_fposvecs)
            self.main_data = tmp

    def _get_each_step(self, index):
        init = index * self.total_at
        fin = init + self.total_at
        return self.main_data[init:fin]

    def _set_each_step(self, index, va):
        init = index * self.total_at
        fin = init + self.total_at
        tmar = self.main_data[init:fin]
        if isinstance(va, np.ndarray):
            if tmar.shape == va.shape:
                self.main_data[init:fin] = va
            else:
                print("shape can't apply")
        else:
            print("need ndarray")

    def switch_main_data(self):
        if self.cartvecs is None:
            self._set_cartvecs()
        if self.main_dtype == "fractional":
            self.main_data = self.cartvecs
            self.main_dtype = "cartesian"
            print("set " + self.main_dtype + " vectors into main_data.")
        elif self.main_dtype == "cartesian":
            self.main_data = self.fracvecs
            self.main_dtype = "fractinoal"
            print("set " + self.main_dtype + " vectors into main_data.")
        else:
            self.main_data = self.fracvecs
            self.main_dtype = "fractional"
            print("main_data is unknown, so it enters fractional vectors.")


class XdatFile(XdatBase):
    # it's class the same object as XdatBase class. however, only the way of
    # input is different from XdatBase class.
    # read_data method functions when it loads data from XDATCAR file.
    # Xdatcar instance is based on the following attribute values.
    # iniline, latvecs, elm_li, natm_li, total_at, fractvecs, self.total_step
    # moreover, it sets cartvecs, main_data.

    def read_data(self, fpath):
        with open(fpath, "r") as read:
            self.iniline = []
            self.iniline.append(read.readline())
            self.iniline.append(read.readline())
            self.latvecs = np.loadtxt(itrt.islice(read, 0, 3))
            self.elm_li = read.next().split()
            self.natm_li = [int(anum) for anum in read.next().split()]
            self.total_at = sum(self.natm_li)
            va = self.total_at + 1
            vecs_txt = (vec for num, vec in enumerate(read, 0)
                        if not num % va == 0)
            self.fracvecs = np.loadtxt(vecs_txt)
            self.total_step = len(self.fracvecs) / self.total_at


class XdatDict(XdatBase):
    # it's class the same object as XdatBase class. however, only the way of
    # input is different from XdatBase class.
    # Xdatcar instance is based on the following attribute values.
    # iniline, latvecs, elm_li, natm_li, total_at, fractvecs, self.total_step
    # moreover, it sets cartvecs, main_data.
    def read_data(self, **kwargs):
        # attribute dictionary includes "natm_li, elm_li, fractvecs, iniline,
        # latvecs, total_at, total_step"
        iniline = kwargs.pop("iniline", None)
        if not isinstance(iniline, list) and len(iniline) == 2:
            sys.stderr.write("iniline is not appropriate type.\n")
            sys.exit(2)
        self.iniline = iniline
        latvecs = kwargs.pop("latvecs", None)
        if not isinstance(latvecs, np.ndarray):
            sys.stderr.write("latvecs is not appropriate type.\n")
            sys.exit(2)
        self.latvecs = latvecs
        natm_li = kwargs.pop("natm_li", None)
        if not isinstance(natm_li, list) and isinstance(natm_li[0], int):
            sys.stderr.write("natm_li is not appropriate type.\n")
            sys.exit(2)
        self.natm_li = natm_li
        elm_li = kwargs.pop("elm_li", None)
        if not isinstance(elm_li, list) and isinstance(elm_li[0], str):
            sys.stderr.write("natm_li is not appropriate type.\n")
            sys.exit(2)
        self.elm_li = elm_li
        fractvecs = kwargs.pop("fractvecs", None)
        if not isinstance(fractvecs, np.ndarray):
            sys.stderr.write("natm_li is not appropriate type.\n")
            sys.exit(2)
        self.fractvecs = fractvecs
        if kwargs:
            raise TypeError("Unexpected **kwargs: %r" % kwargs)
        self.total_at = np.sum(self.natm_li)
        self.total_step = len(self.fracvecs) / self.total_at


class Xdatcar(XdatFile, XdatDict):
    def __init__(self, data_to_load):
        if os.path.exists(data_to_load):
            XdatFile.__init__(self, data_to_load)
        elif isinstance(data_to_load, dict):
            XdatDict.__init__(self, data_to_load)
        else:
            sys.stderr.write("can't load data.\n"
                             "data type is not appropriate.\n")
            sys.exit(2)


class XdatCheckedT(Xdatcar):

    def __init__(self, fpath):
        super(XdatCheckedT, self).__init__(fpath)
        self._set_cartvecs()
        self.main_data = self.cartvecs

    def set_probable_Tvecs(self, cutoff_dist):
        self.cutoff_dist = cutoff_dist
        mx_dist_in_Ucell = self._get_mx_dist()
        v_comp_l = []
        for one_num in range(3):
            v_comp = self._get_vertical_vec_component(one_num)
            v_comp_l.append(v_comp)
        probable_enlarge_vects = self._get_probable_ratio_vecs(
                                                    cutoff_dist,
                                                    mx_dist_in_Ucell,
                                                    v_comp_l)
        probable_Tvecs = np.dot(probable_enlarge_vects, self.latvecs)
        norm_info = np.apply_along_axis(la.norm, 1, probable_Tvecs)
        probable_Tvecs = probable_Tvecs[norm_info <= (mx_dist_in_Ucell +
                                        self.cutoff_dist)]
        self.probable_Tvecs = probable_Tvecs

    def gen_cdenv_act_cutoff(self, step_li, error_va=1.0e-6):
        step_li
        cutoff_dist = self.cutoff_dist
        for one_step in step_li:
            step_posvecs = self._get_each_step(one_step)
            for a_pos in step_posvecs:
                tmp_gene = (step_posvecs + tvec for tvec in
                            self.probable_Tvecs)
                probable_spcell_pvecs = np.vstack(tmp_gene)
                probable_pvecs = probable_spcell_pvecs - a_pos
                norm_info = np.apply_along_axis(la.norm,
                                                1,
                                                probable_pvecs)
                cond1 = norm_info <= cutoff_dist
                cond2 = norm_info >= error_va
                cond = np.logical_and(cond1, cond2)
                matched_norm = norm_info[cond]
                sort_cond = np.argsort(matched_norm)
                matched_pvecs = probable_pvecs[cond]
                sorted_pvecs = matched_pvecs[sort_cond]
                yield sorted_pvecs

    def _get_mx_dist(self):
        candidate_li = []
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                cand = self.latvecs[0] + i*self.latvecs[1] + j*self.latvecs[2]
                candidate_li.append(cand)
        cand_mat = np.vstack(candidate_li)
        max_dist = np.max(np.apply_along_axis(la.norm, 1, cand_mat))
        return max_dist

    def _get_vertical_vec_component(self, target_num):
        lvects = self.latvecs
        target_vec = lvects[target_num]
        cond = np.ones(len(lvects))
        cond[target_num] = 0
        cond = cond.astype(np.bool)
        ref_vecs = lvects[cond]
        vertical_vec = reduce(np.cross, ref_vecs)
        normal_vec = vertical_vec / la.norm(vertical_vec)
        vertical_vec_component = np.dot(target_vec, normal_vec)
        abs_vcomponent = np.abs(vertical_vec_component)
        return abs_vcomponent

    def _get_probable_ratio_vecs(self, cutoff_dist, mx_dist,
                                 vertical_component_list):
        # for example(1,2,3) act lattice vectors
        v_compo_ar = np.array(vertical_component_list)
        ref_dist = mx_dist + cutoff_dist
        enlarge_ratio = np.ceil(ref_dist / v_compo_ar)
        enlarge_ratio = enlarge_ratio.astype(np.int64)
        probable_enlarge_rat_l = []
        for a_num in range(-enlarge_ratio[0],
                           enlarge_ratio[0] + 1):
            for b_num in range(-enlarge_ratio[1],
                               enlarge_ratio[1] + 1):
                for c_num in range(-enlarge_ratio[2],
                                   enlarge_ratio[2] + 1):
                    prob_rvec = np.array([a_num, b_num, c_num])
                    probable_enlarge_rat_l.append(prob_rvec)
        prob_rvecs = np.vstack(probable_enlarge_rat_l)
        return prob_rvecs
