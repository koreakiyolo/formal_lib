#!/usr/bin/env python3
# !coding:utf-8


import pandas as pd
from pandas import DataFrame
import numpy as np
import os

"""
how to calculate the cooling rate.
x(tn): tn is the moment of arc welding.
T[t(x[n+1])] - t[t(x[n])] / delta(t)
it's based on the following formulation.
delta(t) = x[n+1] - x[n] / V(x)

how to calculate the temprature gradient. for example, the following shows
case of x-direction: [T{x(n+1)} - T{x(n)}]/delta(x)

"""


DIST_COL = "distance(m)"
TEMPE_COL = "temperature(C0)"
GRADIENT_TCOL = "grad_t(K/m)"
NORM_GR_XCOL = "norm_grad_xi()"
NORM_GR_YCOL = "norm_grad_y()"
NORM_GR_ZCOL = "norm_grad_z()"
NORM_COLS = [NORM_GR_XCOL, NORM_GR_YCOL, NORM_GR_ZCOL]

VTIME_COL = "virtual_time(s)"
R_COL = "COOLING_RATE(K/s)"


class AnalyzeGR(object):
    def __init__(self, fcsv):
        self.raw_df = pd.read_csv(fcsv)
        print("it shows the steps of setting parameters.\n"
              "first, set temprature range by using set_tempe_range.\n"
              "second, set welding speed")

    def set_tempe_range(self, tempe_tp):
        min_t, max_t = tempe_tp
        c1 = self.raw_df[TEMPE_COL] >= min_t
        c2 = self.raw_df[TEMPE_COL] <= max_t
        total_cond = np.logical_and(c1, c2)
        self.tempe_extracted_df = self.raw_df[total_cond]

    def set_welding_speed(self, speed):
        self.welding_speed = speed
        tmp_dist_nplus1 = self.tempe_extracted_df[DIST_COL][1:]
        tmp_dist_n = self.tempe_extracted_df[DIST_COL][0:-1]
        dif_dist_ar = tmp_dist_nplus1 - tmp_dist_n
        dif_time = dif_dist_ar / self.welding_speed
        self.dif_time = dif_time
        tmp_tmpe_nplus1 = self.tempe_extracted_df[TEMPE_COL][1:]
        tmp_tmpe_n = self.tempe_extracted_df[TEMPE_COL][0:-1]
        self.tempe_dif = tmp_tmpe_nplus1 - tmp_tmpe_n
        tmp = np.cumsom(dif_time)
        time_ar = np.empty(np.len(tmp) + 1)
        time_ar[1:] = tmp
        time_ar[0] = 0
        self.tempe_extracted_df[VTIME_COL] = time_ar

    def set_R(self):
        tmp_R_ar = self.tempe_dif / self.dif_time
        R_ar = np.empty(len(tmp_R_ar) + 1)
        R_ar[0:-1] = tmp_R_ar
        R_ar[-1] = np.nan
        self.tempe_extracted_df[R_COL] = R_ar

    def set_total(self, tempe_tp, speed):
        self.set_tempe_range(tempe_tp)
        self.set_welding_speed(speed)
        self.set_R()

    def output_result(self, opath):
        tmp_R = self.tempe_extracted_df[R_COL]
        tmp_G = self.tempe_extracted_df[GRADIENT_TCOL]
        result = np.vstack(tmp_R, tmp_G).T
        result_R = result[:, 0]
        result_G = result[:, 1]
        tmp = result_R[~np.nan(result_R)]
        averaged_R = np.average(tmp)
        tmp = result_G[~np.nan(result_G)]
        averaged_G = np.average(tmp)
        with open(opath, "w") as write:
            msg = "# averaged_R = " + repr(averaged_R)
            write.write(msg)
            msg = "# averaged_G = " + repr(averaged_G)
            write.write(msg)
            msg = "# result_R result_G"
            write.write(msg)
            np.savetxt(write, result)

    def output_extended_result(self, opath):
        tmp_R = self.tempe_extracted_df[R_COL].get_values()
        tmp_G = self.tempe_extracted_df[GRADIENT_TCOL].get_values()
        tmp_G_ncomps = self.tempe_extracted_df[NORM_COLS].get_values()
        norm_G = np.diag(tmp_G)
        G_comps_ar = np.dot(norm_G, tmp_G_ncomps)
        R_ar = tmp_R.reshape(-1, 1)
        result = np.hstak((R_ar, G_comps_ar))
        averaged_result = np.apply_along_axis(average_skip_nan, 0, result)
        tmp = np.vstack([averaged_result, result])
        colnms = ["R", "G_x", "G_y", "G_z"]
        target_df = DataFrame(tmp, columns=colnms)
        tmp_ix = target_df.index.tolist()
        tmp_ix[0] = "average"
        target_df.index = tmp_ix
        target_df.to_csv(opath, index=True)


def average_skip_nan(self, oneD_ar):
    tmp = oneD_ar[~np.nan(oneD_ar)]
    averaged_va = np.average(tmp)
    return averaged_va


if __name__ == "__main__":
    import argparse
    msg = "it calculate G R data from csv_data_file applying a coordinate."
    parser = argparse.ArgumentParser(description=msg, fromfile_prefix_chars)
    parser.add_argument("--csv_input", type=str, nargs="?", required=True)
    parser.add_argument("--bead_velocity", type=float, nargs="?",
                        required=True)
    parser.add_argument("--wpath_result", type=str, nargs="?", default=None)
    temp_mes = "at least one argumet of the groups must be set."
    tempe_group = parser.add_argument_group("temprature parameter",
                                            description=temp_mes)
    tempe_group.add_argument("--celcius_range", type=float,
                             nargs=2, default=None)
    tempe_group.add_argument("--kelvin_range", type=float,
                             nargs=2, default=None)
    parser.parse_args()
    CSV_INPUT = parser.csv_input
    BEAD_VELOCITY = parser.bead_velocity
    WPATH_RESULT = parser.wpath_result
    CELCIUS_RANGE = parser.celcius_range
    KELVIN_RANGE = parser.kelvin_range
