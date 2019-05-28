#!/usr/bin/env python
# !coding:utf-8

import numpy as np
import argparse
import os
import sys
import itertools

def convert_idfour_to_idthree(ar_idfour, pl_or_dir="direction"):
    if pl_or_dir == "plane":
        ar_idthree = ar_idfour[[0,1,3]]
    elif pl_or_dir == "direction":
        ar_idthree = np.array([(ar_idfour[0] - ar_idfour[2]),
                               (ar_idfour[1] - ar_idfour[2]),
                               ar_idfour[3]])
    else:
        sys.stderr.write("arg2(pl_or_dir) must be set plane or direction.\n")
    return ar_idthree


def convert_idthree_to_idfour(ar_idthree, pl_or_dir="direction"):
    if pl_or_dir == "plane":
        h = ar_idthree[0]
        k = ar_idthree[1]
        i = - (h + k)
        l = ar_idthree[2]
        ar_idfour = np.array([h, k, i, l])
    elif pl_or_dir == "direction":
        u_dash = ar_idthree[0]
        v_dash = ar_idthree[1]
        w_dash = ar_idthree[2]
        h = 2*u_dash - v_dash
        k = - u_dash + 2*v_dash
        i = - (u_dash + v_dash)
        l = 3 * w_dash
        ar_idfour = np.array([h, k, i, l])
    else:
        sys.stderr.write("arg2(pl_or_dir) must be set plane or direction.\n")
    return ar_idfour

def get_equivarent_idfour_mat(ar_idfour):
    bot_id = ar_idfour[0:3]
    c_compo = ar_idfour[3]
    botid_li = []
    for tmp_comb_tp in itertools.permutations(bot_id):
        minus_comb_tp = tuple([-num for num in tmp_comb_tp])
        botid_li.append(tmp_comb_tp)
        botid_li.append(minus_comb_tp)
    botid_set = set(botid_li)
    li_for_ar = []
    for one_comb in botid_set:
        plus_id = tuple(list(one_comb) + [c_compo])
        minus_id = tuple(list(one_comb) + [-c_compo])
        li_for_ar.append(plus_id)
        li_for_ar.append(minus_id)
    set_for_ar = set(li_for_ar)
    return np.array(list(set_for_ar))

def get_equivarent_idthree_mat(ar_idthree, dir_or_pl):
    ar_idfour = convert_idthree_to_idfour(ar_idthree, dir_or_pl)
    eq_idfour_mat = get_equivarent_idfour_mat(ar_idfour)
    idthree_iter = (convert_idfour_to_idthree(one_idfour, dir_or_pl) 
                  for one_idfour in eq_idfour_mat)
    return np.vstack(idthree_iter)


def get_smallesti_integer_id(one_ar):
    if not isinstance(one_ar, np.ndarray):
        one_ar = np.array(one_ar)
    one_ar = one_ar.astype(np.int64)
    common_div = reduce(get_greatest_common_div, one_ar)
    return one_ar / common_div


def get_greatest_common_div(a, b):
    # calculate greatest commmon divisor
    a, b = np.abs((a, b))
    max_va = np.max((a, b))
    min_va = np.min((a, b))
    while min_va:
        max_va, min_va = min_va, max_va%min_va
    return max_va


def cnvt_ar(strings, change_fn=int):
    # this functions isrelated to argparse.
    return np.array([change_fn(one) for one in strings.split()])


class TwinInfo(object):
    def __init__(self, twininfo_f):
        message = "this parser is made for"\
                  " class object (Twin_Info) "\
                  "and parser load data only "\
                  "from file_object"
        parser = argparse.ArgumentParser(description=message,
                                         fromfile_prefix_chars="@")
        parser.add_argument("--k1_plane", type=cnvt_ar, nargs="?")
        parser.add_argument("--k2_plane", type=cnvt_ar, nargs="?")
        parser.add_argument("--eta1", type=cnvt_ar, nargs="?")
        parser.add_argument("--eta2", type=cnvt_ar, nargs="?")
        parser.add_argument("--matrix_spcell_ratio", type=cnvt_ar, nargs="?",
                            default=np.array([1, 1, 1]))
        ## add the other input information 
        self.parser = parser
        self.load_twininfo_fromfile(twininfo_f)
        self.cnvt_idfour_idthree()

    def load_twininfo_fromfile(self, twininfo_f):
        if not os.path.exists(twininfo_f):
            sys.stderr.write("twin information file don't exist.\n")
            sys.exit(2)
        self.args = self.parser.parse_args(["@" + twininfo_f])
        
    def cnvt_idfour_idthree(self):
        self.k1p_idthree = convert_idfour_to_idthree(self.args.k1_plane, "plane")
        self.k2p_idthree = convert_idfour_to_idthree(self.args.k2_plane, "plane")
        eta1_idthree = convert_idfour_to_idthree(self.args.eta1, "direction")
        self.eta1_idthree = get_smallesti_integer_id(eta1_idthree)
        eta2_idthree = convert_idfour_to_idthree(self.args.eta2, "direction")
        self.eta2_idthree = get_smallesti_integer_id(eta2_idthree)
        sight_dir_id = np.cross(self.k1p_idthree, self.k2p_idthree)
        self.sight_dir_id = get_smallesti_integer_id(sight_dir_id)
        self.mat_act_hexalatvecs = np.vstack((self.eta1_idthree,
                                              self.sight_dir_id,
                                              self.eta2_idthree))
        self.to_supercell()
    def to_supercell(self):
        matrix_spcell_ratio = self.args.matrix_spcell_ratio
        if len(matrix_spcell_ratio) != 3:
            sys.stderr.write("matrix_spcell_ratio must have three"
                             " component.\n"
                             "can't convert unitcell to spcell by usinng"
                             " to_supercell method.\n")
            sys.exit(2)
        trfm_mat = np.diag(matrix_spcell_ratio)
        self.mat_act_hexalatvecs= np.dot(self.mat_act_hexalatvecs, trfm_mat)
