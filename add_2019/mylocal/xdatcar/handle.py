#!/usr/bin/env python
# !:coding:utf-8

# formal library
import numpy as np
from itertools import izip
from copy import deepcopy
import sys

# my library
from core import Xdatcar
import core as xdatcar


def merge_xdatcar(xdatcar_ins_li, confirm=False, memory_save=False):
    # if confirm_va is True, it confirms latvecs and inequivalent atom number.
    # if memory_save va is True, this function eliminate a xdatcar instance
    # every time it process such a instance.
    if confirm:
        confirm_sametype_xdatins(xdatcar_ins_li)
    input_dict = {}
    input_dict["iniline"] = xdatcar_ins_li[0].iniline
    input_dict["latvecs"] = xdatcar_ins_li[0].latvecs
    input_dict["elm_li"] = xdatcar_ins_li[0].elm_li
    input_dict["natom_li"] = xdatcar_ins_li[0].natm_li
    fvecs_gene = (ins.fractvecs for ins in xdatcar_ins_li)
    total_fvecs = np.vstack(fvecs_gene)
    input_dict["fractvecs"] = total_fvecs
    if memory_save:
        del xdatcar_ins_li
    return Xdatcar(input_dict)


def divide_xdatcar_to_multi(xdatcar_ins, li_with_step_li, memory_save=False):
    if not isinstance(xdatcar_ins, xdatcar.XdatBase):
        sys.stderr.write("you must input XdatBase instance to divide"
                         " function.\n")
        sys.exit(2)
    input_dict = {}
    input_dict["iniline"] = xdatcar_ins.iniline
    input_dict["latvecs"] = xdatcar_ins.latvecs
    input_dict["elm_li"] = xdatcar_ins.elm_li
    input_dict["natom_li"] = xdatcar_ins.natm_li
    input_dict_li = [deepcopy(input_dict) for _ in range(len(li_with_step_li))]
    output_xdatcar_li = []
    for input_dict, extract_li in izip(input_dict_li, li_with_step_li):
        input_dict["fractvecs"] = xdatcar_ins[extract_li]
        output_xdatcar_li.append(Xdatcar(input_dict))
    if memory_save:
        del xdatcar_ins
    return output_xdatcar_li


def confirm_sametype_xdatins(xdatcar_ins_li, tolerance=1.0e-5):
    # it confirms (1) whether all instances are Xdatcar
    # (2) whether all instances have the same latvecs.
    # (3) whether all instances have the same elm_li and natom_li
    # if there is no problem, function returns true.
    # part(1) check instance type
    confirm_li = [isinstance(ins, xdatcar.XdatBase) for ins in
                  xdatcar_ins_li]
    tmp_cond = np.count_nonzero(confirm_li)
    if tmp_cond != len(tmp_cond):
        sys.stderr.write("you must input list with xdatcar instances.\n")
        raise TypeError
    # part(2) check latvecs of all instance
    latvecs_confirm_gene = (ins.latvecs for ins in xdatcar_ins_li)
    base_latvecs = next(latvecs_confirm_gene)
    condva_li = []
    for one_latvecs in latvecs_confirm_gene:
        va = np.max(one_latvecs - base_latvecs)
        condva_li.append(va)
    if np.max(condva_li) >= tolerance:
        sys.stderr.write("you must input with xdatcar instances with the"
                         " same latves.\n")
        raise TypeError
    # part(3)
    condli_withelm_tp = [tuple(ins.elm_li) for ins in xdatcar_ins_li]
    condli_withnatom_tp = [tuple(ins.natom_li) for ins in xdatcar_ins_li]
    base_elm_tp = condli_withelm_tp[0]
    for an_elm_tp in condli_withelm_tp[1:]:
        if base_elm_tp != an_elm_tp:
            sys.stderr.write("xdatcar instances you have inputed don't have"
                             " the same elm_li.")
            raise TypeError
    base_natom_tp = condli_withnatom_tp
    for an_natom_tp in condli_withnatom_tp[1:]:
        if base_natom_tp != an_natom_tp:
            sys.stderr.write("xdatcar instances you have inputed don't have"
                             " the same elm_li.")
            raise TypeError
    return True
