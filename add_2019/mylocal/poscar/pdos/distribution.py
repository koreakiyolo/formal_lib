#!/usr/bin/env python
# !coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
import sys
import os


def calc_integral_dist(x_array, y_array):
    delta_x = x_array[1] - x_array[0]
    mean_y = (y_array[1:] + y_array[0:-1]) / 2.0
    value = delta_x * np.sum(mean_y)
    return value


def calc_average(x_array, y_array):
    return calc_nmom(x_array, y_array, 1)


def calc_dispersion(x_array, y_array):
    mom2 = calc_nmom(x_array, y_array, 2)
    mom1 = calc_nmom(x_array, y_array, 1)
    disp = (mom2 - mom1**2)
    return disp


def calc_nmom(x_array, y_array, n_mom):
    # it calculates n moment of distribution
    # value has been standardized
    n_mom_va = calc_nmom_bfstandard(x_array, y_array, n_mom)
    stand_ratio = calc_nmom_bfstandard(x_array, y_array, 0)
    value = n_mom_va / stand_ratio
    return value


def calc_nmom_bfstandard(x_array, y_array, n_mom):
    # it calculates n moment of distribution.
    # value has't been standardized
    delta_x = x_array[1] - x_array[0]
    coeff_ratio = x_array ** n_mom
    fin_coeff = (coeff_ratio[1:] + coeff_ratio[0:-1]) / 2.0
    mean_y = (y_array[1:] + y_array[0:-1]) / 2.0
    total_va = np.dot(fin_coeff, mean_y)
    value = delta_x * total_va
    return value


def calc_dif_of_dists(d1_xar, d1_yar, d2_xar, d2_yar):
    if len(d1_xar) != len(d2_xar):
        sys.stderr.write("error occurs in fn(calc_dif_if_dists).\n"
                         "you must enter the same lengths of two "
                         "distributions")
        sys.exit(2)
    dif_x = np.sum(d2_xar - d1_xar)
    if dif_x > 1.0e-7:
        sys.stderr.write("error occurs in fn(calc_dif_if_dists).\n"
                         "you must two distributions which are in "
                         "the samerange\n")
        sys.exit(2)
    micro_dif_yar = np.abs(d1_yar - d2_yar)
    tmp_deltax_ar = d1_xar[1:] - d2_xar[0:-1]
    delta_xar = np.hstack((tmp_deltax_ar, tmp_deltax_ar[-1]))
    ans = np.dot(delta_xar, micro_dif_yar)
    return ans


class Dist(object):
    # Dist object manage distributions.
    # it can load data from file object or x_ar, y_ar.
    def __init__(self, dist_fpath_or_tp):
        if isinstance(dist_fpath_or_tp, str):
            if not os.path.exists(dist_fpath_or_tp):
                sys.stderr.write("you must correct path of Dist object.\n")
                sys.exit(2) 
            self._load_dist(dist_fpath_or_tp)
            self.moment_dict = {}
        elif isinstance(dist_fpath_or_tp, tuple):
            self.dist_x = dist_fpath_or_tp[0]
            self.dist_y = dist_fpath_or_tp[1]
            self.moment_dict = {}

    def _load_dist(self, dist_fpath):
        dist = np.loadtxt(dist_fpath)
        self.dist_x = dist[:, 0]
        self.dist_y = dist[:, 1]

    def set_integral_dist(self):
        va_integ = calc_integral_dist(self.dist_x, self.dist_y)
        self.integraled_va = va_integ

    def set_nmoment(self, *args):
        moment_itr = (int(num) for num in args)
        new_dict = {nmom: calc_nmom(self.dist_x, self.dist_y, nmom) for nmom
                    in moment_itr}
        self.moment_dict = new_dict

    def set_probability_dist(self):
        self.set_integral_dist()
        self.prob_xarray = self.dist_x
        self.prob_yarray = self.dist_y / self.integraled_va

    def standard_set(self):
        self.set_nmoment([0, 1, 2])
        self.set_integral_dist()
        self.set_probability_dist()

    def plot_graph(self, **kwargs):
        x_ratio = kwargs.pop("xratio", None)
        y_ratio = kwargs.pop("yratio", None)
        if kwargs:
            raise TypeError("Unexpected **kwargs: {}".format(kwargs))
        x_ar = self.dist_x
        y_ar = self.dist_y
        if x_ratio is not None:
            x_ar = x_ratio * x_ar
        if y_ratio is not None:
            y_ar = y_ratio * y_ar
        plt.plot(x_ar, y_ar)
