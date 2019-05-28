#!/usr/bin/env python
# !coding:utf-8

# formal lib
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
import sys

# my_lib
from .. import POSCAR
from . import distribution

# plot_info
tmp_plotstyle = [[], [2, 1], [1, 3], [2, 2], [2, 3], [2, 3], [2, 4],
                 [2, 4], [3, 3], [3, 4], [3, 4], [3, 4]]
DICT_WITH_SUB_PLOT_INFO = dict(zip(range(1, 10), tmp_plotstyle))
DICT_WITH_SUB_PLOT_INFO[16] = [4,4]
# Boltzmann's constant
KB = 1.38064852*1e-23
# electronic elementary charge
ELECTRO_E = 1.6021766208*1e-19
# temprature of MD simulation
T = 600
# PAI
PI = np.pi
# ratio to convert power spectrum to DOS only when using the same unitcell.
RATIO_POW_TO_DOS = 2 * ELECTRO_E / (KB*T)


class PdosOrPpower(object):
    # this class functions is shown in the following.
    # 0.manage various distributions.
    # 1.compare partial dos or partial power spectrum with reference
    #   distribution.
    # 2.calculate the moment of distibutions.
    # 3.plot distritbutions with reference distribution.
    def __init__(self, pd_pp_fpath, reference_fpath=None):
        self.reference_type = None
        self._set_df_with_pd_pp(pd_pp_fpath)
        if reference_fpath is None:
            pass
        else:
            self._set_refdf_with_pd_pp(reference_fpath)

    def _set_df_with_pd_pp(self, pd_pp_fpath):
        tmp_dists = np.loadtxt(pd_pp_fpath)
        columns_nm = ["frequency"]
        atom_nm = tmp_dists.shape[1]
        atom_nm_li = range(atom_nm - 1)
        columns_nm.extend(atom_nm_li)
        self.df_with_pd_pp = DataFrame(tmp_dists, columns=columns_nm)

    def _set_refdf_with_pd_pp(self, ref_pd_pp_fpath):
        tmp_dists = np.loadtxt(ref_pd_pp_fpath)
        columns_nm = ["frequency"]
        dist_nm = tmp_dists.shape[1]
        dist_nm_li = range(dist_nm - 1)
        columns_nm.extend(dist_nm_li)
        self.refdf_with_pd_pp = DataFrame(tmp_dists, columns=columns_nm)
        if dist_nm == 1:
            self.reference_type = "one_dist"
            print("set one reltive distribution.\n")
        elif dist_nm == (len(self.df_with_pd_pp.columns) - 1):
            self.reference_type = "same_num_dist"
            print("set the same number of relative distributions "
                  "as the number of pdos or ppower specturum")
        else:
            self.reference_type = "unknown_multi"
            print("set multiple distributions.\n"
                  "you must choose the stype of plot.\n")

    def _get_moment_df_distirbution(self, input_df, moment_li=[0, 1, 2]):
        index_nm_li = range(len(input_df.columns[1:]))
        df_list = []
        for column_nm in input_df.columns[1:]:
            nmom_li = []
            for nmom in moment_li:
                value = distribution.calc_nmom(np.array(input_df["frequency"]),
                                               np.array(input_df.loc[:,column_nm]),
                                               nmom)
                nmom_li.append(value)
            df_list.append(nmom_li)
        moment_df = DataFrame(df_list, columns=moment_li, index=index_nm_li)
        return moment_df

    def set_moment_df(self):
        self.moment_df = self._get_moment_df_distirbution(self.df_with_pd_pp)
        if hasattr(self, "refdf_with_pd_pp"):
            self.refmoment_df = self._get_moment_df_distirbution(
                                            self.refdf_with_pd_pp)

    def customed_plot_pp_pd_to_graph(self, dist_id_li=[], xlim=[0, 10],
                                     ref_id_li=[], show=True):
        frequency = self.df_with_pd_pp["frequency"]
        graph_num = len(dist_id_li)
        if graph_num == 0:
            # df.iloc indicate id number
            # df.loc indicate id name
            print("plot atom num1")
            plt.plot(frequency, self.df_with_pd_pp.iloc[:, 0])
            for ref_at_nm in ref_id_li:
                    plt.plot(self.refdf_with_pd_pp["frequency"],
                             self.relative_df_with_pd_pp.loc[:, ref_at_nm])
                    plt.xlim(*xlim)
        else:
            graph_conds = DICT_WITH_SUB_PLOT_INFO[graph_num]
            for num, atom_index in enumerate(dist_id_li):
                plt.subplot(graph_conds[0], graph_conds[1], num + 1)
                plt.plot(self.df_with_pd_pp["frequency"],
                         self.df_with_pd_pp.loc[:, atom_index], "b")
                for ref_distnm in ref_id_li:
                    plt.plot(self.refdf_with_pd_pp["frequency"],
                             self.refdf_with_pd_pp.loc[:, ref_distnm],
                             "g")
                    plt.xlim(*xlim)
        if show:
            plt.show()

    def make_pppd_graphs(self):
        if self.reference_type is None:
            sys.stderr.write("method(make_pppd_graphs) is immature.\n")
            sys.exit(2)
        elif self.reference_type == "one_dist":
            sys.stderr.write("method(make_pppd_graphs) is immature.\n")
            sys.exit(2)
        elif self.reference_type == "same_num_dist":
            sys.stderr.write("method(make_pppd_graphs) is immature.\n")
            sys.exit(2)
        elif self.reference_type == "unknown_multi":
            sys.stderr.write("method(make_pppd_graphs) is immature.\n")
            sys.exit(2)


class PosWithPdosEtc(POSCAR, PdosOrPpower):
    # calc
    def __init__(self, poscar_f, pdos_fpath, ref_distpath=None):
        POSCAR.__init__(self, poscar_f)
        Pdos_or_Ppower.__init__(self, pdos_fpath, ref_distpath)
        self.set_moment_df()

    def sum_ensemble_equivalent_atom(self, list_with_eqatom_idli):
        for eqatom_idli in list_with_eqatom_idli:
            averaged_dist = self.df_with_pd_pp.loc[:, eqatom_idli].apply(np.mean, 1)
            for one_atom in eqatom_idli:
                self.df_with_pd_pp.loc[:, one_atom] = averaged_dist
        self.set_moment_df()

"""
def plot_graph_with_two_axis(self,x_index="z",y_index="moment_1",relevant_value=0.0):
        axis_dict=dict(zip(list("xyz"),[0,1,2]))
        x_array=self.cartesian_position_vectors_df_with_moment_info[x_index]
        y_array=self.cartesian_position_vectors_df_with_moment_info[y_index]-relevant_value
        plt.xlim(0,la.norm(self.lattice_vectors_act_cartesian_with_norm[axis_dict[x_index]]))
        plt.plot(x_array,y_array,"bo")
        plt.show()
"""
