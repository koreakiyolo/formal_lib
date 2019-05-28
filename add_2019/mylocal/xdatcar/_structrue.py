#!/usr/bin/env python
# !coding:utf-8

import numpy as np
from numpy import linalg as la
import scipy as scp


def calc_angle(a_vec, b_vec):
    prod = np.dot(a_vec, b_vec)
    a = la.norm(a_vec)
    b = la.norm(b_vec)
    cos = prod/(a*b)
    rad = scp.arccos(cos)
    deg = scp.rad2deg(rad)
    return deg


def cnvt_latvecs_in_easiest_way(latvecs):
    a_vec = latvecs[0]
    b_vec = latvecs[1]
    c_vec = latvecs[2]
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


def cnvt_latvecs_norm_angle(latvecs):
    norm_ar = np.apply_along_axis(la.norm, 1, latvecs)

    def tmp_gene():
        while True:
            yield np.ones(3, np.bool)
    gene = tmp_gene()
    angle_li = []
    for i in range(3):
        cond = gene.next()
        cond[i] = False
        two_lats = latvecs[cond]
        deg = calc_angle(two_lats[0], two_lats[1])
        angle_li.append(deg)
    angle_ar = np.array(angle_li)
    return (norm_ar, angle_ar)


def compare_latvecs(latvecs_li, ang_tole=0.001, norm_tole=1.0e-6):
    norm_angle_li = [cnvt_latvecs_norm_angle(latvecs)
                     for latvecs in latvecs_li]
    base = norm_angle_li[0]
    ref_li = norm_angle_li[1:]

    def norm_test(ref_norm, num):
        msg = "norm mismatch" + "at list " + str(num)
        tmp = np.testing.assert_almost_equal(base[0],
                                             ref_norm,
                                             norm_tole,
                                             msg)
        return tmp

    def angle_test(ref_angle, num):
        msg = "angle mismatch" + "at list " + str(num)
        tmp = np.testing.assert_almost_equal(base[1],
                                             ref_angle,
                                             ang_tole,
                                             msg)
        return tmp
    for num, ref in enumerate(ref_li, 1):
        r_norm, r_angle = ref
        norm_test(r_norm, num)
        angle_test(r_angle, num)


def compare_tpli(tp_li):
    base = tp_li[0]
    for num, ref in enumerate(tp_li):
        assert base == num, "tp[0] and tmp[" + str(num) + "] is different"
