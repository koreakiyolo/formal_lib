#!/uxr/bin/env python
# !coding:utf-8

# formal_lib
import numpy as np
import pandas as pd
from numpy import linalg as la
from pandas import DataFrame

# my_lib
from . import POSCAR


def get_cos(avec, bvec):
    cos = np.dot(avec, bvec) / (la.norm(avec)*la.norm(bvec))
    return cos


class PosAdpIdp(POSCAR):
    def __init__(self, pospath, adpfile):
        super(PosAdpIdp, self).__init__(pospath)
        self.set_latparam_dict(self.latvecs)
        atoms_adp_ar = np.loadtxt(adpfile)
        isodisp_ar = np.apply_along_axis(self.calc_isoparam_from_ADP,
                                         1, atoms_adp_ar)
        isodisp_ar = isodisp_ar.reshape(-1, 1)
        self.total_disp = np.hstack((atoms_adp_ar, isodisp_ar))
        self.set_cartesian_cooridinate_df()
        self.set_df_fpos_disp()

    def set_df_fpos_disp(self):
        column_li = ["xx", "yy", "zz",
                     "yz", "zx", "xy", "isodisp"]
        self.column_li = column_li
        self.df_adp_idp = DataFrame(self.total_disp,
                                    index=self.elements_array,
                                    columns=column_li)
        self.df_cpos_disp = pd.concat((self.df_cpos, self.df_adp_idp),
                                      axis=1).reset_index()

    def set_cartesian_cooridinate_df(self):
        cart_posvecs = np.dot(self.fractional_pos_vecs, self.latvecs)
        self.df_cpos = DataFrame(cart_posvecs, columns=["x", "y", "z"],
                                 index=self.elements_array)

    def set_latparam_dict(self, cartesian_latvecs):
        latvecs = cartesian_latvecs
        latnorm = np.apply_along_axis(la.norm, 1, latvecs)
        cos_alpha = get_cos(latvecs[1], latvecs[2])
        cos_beta = get_cos(latvecs[2], latvecs[0])
        cos_gamma = get_cos(latvecs[0], latvecs[1])
        cos_li = [cos_alpha, cos_beta, cos_gamma]
        ang_li = []
        for cos_va in cos_li:
            angle = np.arccos(cos_va)
            ang_li.append(angle)
        latparam_li = latnorm.tolist() + ang_li
        latparam_li.extend(cos_li)
        key_list = ["a", "b", "c",
                    "alpha", "beta", "gamma",
                    "cos_alpha", "cos_beta", "cos_gamma"]
        latparam_dict = dict(zip(key_list, latparam_li))
        self.latparam_dict = latparam_dict

    def calc_isoparam_from_ADP(self, adp_ar):
        # six_component xx yy zz yz zx xy "" this order is adopted
        # using self.reciprocal or actual lattice_parameter_dict
        U11 = adp_ar[0]
        U22 = adp_ar[1]
        U33 = adp_ar[2]
        U23 = adp_ar[3]
        U13 = adp_ar[4]
        U12 = adp_ar[5]
        rec_norm = np.apply_along_axis(la.norm, 1, self.reciprocal_vecs)
        U11_item = U11 * ((self.latparam_dict["a"]*rec_norm[0]) ** 2)
        U22_item = U22 * ((self.latparam_dict["b"]*rec_norm[1]) ** 2)
        U33_item = U33 * ((self.latparam_dict["c"]*rec_norm[2]) ** 2)
        U12_item = 2 * U12 * (rec_norm[0] * rec_norm[1] *
                              self.latparam_dict["a"] *
                              self.latparam_dict["b"] *
                              self.latparam_dict["cos_gamma"])
        U13_item = 2 * U13 * (rec_norm[0] * rec_norm[2] *
                              self.latparam_dict["a"] *
                              self.latparam_dict["c"] *
                              self.latparam_dict["cos_beta"])
        U23_item = 2 * U23 * (rec_norm[1] * rec_norm[2] *
                              self.latparam_dict["b"] *
                              self.latparam_dict["c"] *
                              self.latparam_dict["cos_alpha"])
        U_eq = 1.0/3.0 * (U11_item + U22_item + U33_item +
                          U12_item + U23_item + U13_item)
        return U_eq

    def average_dispresult_act_list(self, aranged_li_with_indextp):
        stack_li = []
        df_disp = self.df_cpos_disp[self.column_li]
        for index_li in aranged_li_with_indextp:
            tmp = df_disp.ix[index_li]
            ar_vas = tmp[self.column_li]
            averaged_ar = np.average(ar_vas, axis=0)
            stack_li.extend([averaged_ar] * len(index_li))
        new_adp = np.vstack(stack_li)
        self.df_cpos_disp[self.column_li] = new_adp
