#!/usr/bini/env python3


import pandas as pd
from pandas import DataFrame
import numpy as np

GRAIN_NUMCOL = "grain_num"
MPOS_XCOL = "mean_pos_x"
MPOS_YCOL = "mean_pos_y"
DIAMATER_COLS = "diameter"
RATIO_ELLIPS_COL = "aspect_ratio_ellipse_fit"
MAJ_ELIPAXIS_COL = "major_ellip_axis"
MIN_ELIPAXIS_COL = "minor_ellip_axis"
AREA_GRAIN_COL = "area_of_grain"

CAND_COLNMS = set([GRAIN_NUMCOL, MPOS_XCOL, MPOS_YCOL, DIAMATER_COLS,
                   MAJ_ELIPAXIS_COL, MIN_ELIPAXIS_COL, RATIO_ELLIPS_COL,
                   AREA_GRAIN_COL])


class AnalyGrain(object):
    def __init__(self, fcsv, pos_xrange, pos_yrange):
        self.target_df = pd.read_csv(fcsv)

    def set_df_act_posrange(self, pos_xrange, pos_yrange):
        xmin, xmax = pos_xrange
        ymin, ymax = pos_yrange
        cxmin = self.target_df[MPOS_XCOL] >= xmin
        cxmax = self.target_df[MPOS_XCOL] < xmax
        cymin = self.target_df[MPOS_YCOL] >= ymin
        cymax = self.target_df[MPOS_YCOL] < ymax
        tmp = np.vstack([cxmin, cxmax, cymin, cymax]).T
        total_cond = np.max(tmp, axis=1)
        self.extracted_df = self.target_df[total_cond]

    def get_averaged_col(self, colnms):
        averaged_ar = np.average(self.extracted_df[colnms],
                                 axis=0).reshape(1, -1)
        new_col = [nm+"_ave" for nm in colnms]
        averaged_df = DataFrame(averaged_ar, columns=new_col)
        return averaged_df


if __name__ == "__main__":
    import argparse
    msg = "it extract data from grain map"
    parser = argparse.ArgumentParser(description=msg,
                                     fromfile_prefix_chars="@")
    parser.add_argument("colnms", type=str, nargs="*")
    parser.add_argument("--infcsv", type=str, nargs="?")
    parser.add_argument("--ocsv", type=str, nargs="?")
    parser.add_argument("--xpos_range", type=float, nargs=2,
                        required=True)
    parser.add_argument("--ypos_range", type=float, nargs=2,
                        required=True)
    args = parser.parse_args()
    COLNMS = args.colnms
    INFCSV = args.fcsv
    OCSV = args.ocsv
    XPOS_RANGE = args.xpos_range
    YPOS_RANGE = args.ypos_range
    if not CAND_COLNMS.issubset(COLNMS):
        raise AssertionError("you must enter elements included by "
                             " ,".join(CAND_COLNMS))
    analy_grain_ins = AnalyGrain(INFCSV)
    analy_grain_ins.set_df_act_posrange(XPOS_RANGE, YPOS_RANGE)
    outcsv = analy_grain_ins.get_mean_col(COLNMS)
    outcsv.to_csv(OCSV)
