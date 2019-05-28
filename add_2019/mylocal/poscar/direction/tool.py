#!/usr/bin/env python
# !coding:utf-8

import numpy as np
from numpy import linalg as la
import math
import itertools

def get_latinfo_ar(latvecs):
    norm_ar = np.apply_along_axis(la.norm, 1, latvecs)
    iter_pair = itertools.combinations(latvecs, 2)
    angle_li = []
    for i_vec, j_vec in iter_pair:
        angle = calc_directions_angle(i_vec, j_vec)
        angle_li.append(angle)
    angle_ar = np.array(angle_li)
    angle_ar = angle_ar[[2, 1, 0]]
    latinfo_ar = np.hstack((norm_ar, angle_ar))
    return latinfo_ar


def compare_latvecs_ins(latvecs_li, angle_tole=0.001,
                        dist_tole = 1.0e-5):
    latinfo_ar_li = []
    for latvecs in latvecs_li:
        latinfo_ar = get_latinfo_ar(latvecs)
        latinfo_ar_li.append(latinfo_ar)
    base_info = latinfo_ar_li[0]
    tmp_dif_gene = (relative_info - base_info  for relative_info in latinfo_ar_li])
    dif_gene = (la.norm(dif) for dif in tmp_dif_gene)
    cond_li = []
    for one_dif_ar in dif_gene:
        norm_dif = one_dif_ar[0:3]
        angle_dif = one_dif_ar[3:]
        n_cond_ar = norm_dif < dist_tole
        ang_cond_ar = angle_dif < angle_tole
        n_cond = np.min(n_cond)
        ang_cond = np.min(ang_cond_ar)
        cond = np.min(n_cond, ang_cond)
        cond_li.append(cond)
    return cond_li


def cnvt_latvecs_in_easiest_way(ap_latvecs):
    a_vec = ap_latvecs[0]
    b_vec = ap_latvecs[1]
    c_vec = ap_latvecs[2]
    new_latvecs = np.zeros((3, 3))
    new_latvecs[0][0] = np.array([la.norm(a_vec), 0, 0])
    base_vec0 = a_vec / new_latvecs[0][0]
    new_latvecs[1][0] = np.dot(base_vec0, b_vec)
    new_latvecs[1][1] = la.norm(b_vec - (new_latvecs[1][0] * base_vec0))
    base_vec1 = b_vec / la.norm(new_latvecs[1])
    new_latvecs[2][0] = np.dot(base_vec0, c_vec)
    new_latvecs[2][1] = np.dot(base_vec1, c_vec)
    tmp_va_for_compo = c_vec - (new_latvecs[2][0]*base_vec0) - (
                                new_latvecs[2][1]*base_vec1)
    new_latvecs[2][2] = la.norm(tmp_va_for_compo)
    if la.det(new_latvecs) < 0:
        new_latvecs[2] = -new_latvecs[2]
    return new_latvecs


def calc_directions_angle(base_vec, relative_vec):
    denomi = la.norm(base_vec) * la.norm(relative_vec)
    numera = np.dot(base_vec, relative_vec)
    radang = math.acos(numera/denomi)
    degang = math.degrees(radang)
    return degang


def calc_angle_directions_li(base_vec, relative_vecs_ar):
    norm_ar = np.apply_along_axis(la.norm, 1, relative_vecs_ar)
    inner_prod = (np.dot(base_vec, one_vec) for one_vec in relative_vecs_ar)
    inner_prod_ar = np.array(inner_prod)
    cos_ar = inner_prod_ar / norm_ar
    radangle_ar = np.array([math.acos(a_cos) for a_cos in cos_ar])
    degangle_ar = np.degrees(radangle_ar)
    return degangle_ar
