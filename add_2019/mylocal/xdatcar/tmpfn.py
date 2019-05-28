#!/usr/bin/env python
# !coding:utf-8

from xdatcar import Xdatcar
import itertools
import numpy as np
import collections
ELEMENT_LIST = ["H", "He", 
                "Li", "Be", "B", "C", "N", "O", "F", "Ne",
                "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
                "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni",
                "Cu", "Zn", "Ga", "Ge", "As", "Se", "Se", "Br", "Kr",
                "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Te", "Ru", "Rh", "Pd",
                "Ag", "Cd", "In", "Sn", "Sb", "Te", "Br", "Kr"]

def synthesize_fracvecs(fpos_path_li, write_path):
    ini = np.loadtxt(fpos_path_li[0])
    total_num = len(ini) * len(fpos_path_li)
    totalpos = np.zeros((total_num, 3))
    for num, fpath in enumerate(fpos_path_li):
        print(num)
        partial_pos = np.loadtxt(fpath)
        global bcast
        bcast = np.arange(num, total_num, len(fpos_path_li))
        totalpos[bcast] = partial_pos
    np.savetxt(write_path, totalpos)



def get_natom_clayer(posvecs, num):
    c_axis = posvecs[:,2]
    sorted_args = np.argsort(c_axis).tolist()
    ans_li= [sorted_args[i:i + num] 
             for i in range(0, len(sorted_args), 4)]
    return ans_li

def get_natom_clayer_v2(posvecs, num):
    c_axis = posvecs[:,2]
    sorted_args = np.argsort(c_axis).tolist()
    ans_li= [sorted_args[i:i + num] 
             for i in range(0, len(sorted_args), num)]
    dict_with_index = collections.defaultdict(list)
    for one_li, n in itertools.izip(ans_li, itertools.cycle(range(num))):
        dict_with_index[n].extend(one_li)
    layer_index = [dict_with_index[i] for i in range(num)]
    return layer_index

def pickup_one_atom(one_index, li_with_colored_index):
    new_list = [one_index]
    for one_li in li_with_colored_index:
        if one_index in one_li:
            one_li.remove(one_index)
    li_with_colored_index.append(new_list)
    return li_with_colored_index
    
    

class Xdatcar_tmp(Xdatcar):
    def __init__(self, fpath):
        super(Xdatcar_tmp, self).__init__(fpath)

    def _rearange_fracvecs(self, li_with_colored_index):
        rearange_li = []
        for one_li in li_with_colored_index:
            rearange_li.extend(one_li)
        for step in range(self.total_step):
            bef_arange = self._get_each_step(step)
            aft_arange = bef_arange[rearange_li]
            self._set_each_step(step, aft_arange)

    def color_atoms(self, li_with_colored_index):
        same_cl_li = []
        for colored_li in li_with_colored_index:
            same_cl_li.append(len(colored_li))
        self._rearange_fracvecs(li_with_colored_index)
        elm_list = []
        num_list = []
        for elm,num in itertools.izip(ELEMENT_LIST, same_cl_li):
            elm_list.append(elm)
            num_list.append(num)
        self.elm_li = elm_list
        self.natm_li = num_list

    def to_supercell(self, enlaged_ratio_ar):
        enlaged_ratio_ar = np.array(enlaged_ratio_ar)
        sp_latvecs = np.dot(np.diag(enlaged_ratio_ar), self.latvecs)
        self.latvecs = sp_latvecs
        new_fracvecs = self.fracvecs / enlaged_ratio_ar
        for xnum in xrange(enlaged_ratio_ar[0]):
            for ynum in xrange(enlaged_ratio_ar[1]):
                for znum in xrange(enlaged_ratio_ar[2]):
                    Trans_vecs = np.array([xnum, ynum, znum]) / enlaged_ratio_ar.astype(np.float)
                    partial_posvecs = new_fracvecs + Trans_vecs
                    self.fracvecs = partial_posvecs
                    self.write_xdatcar("partial"+str(xnum)+str(ynum)+str(znum)+".vtk")
