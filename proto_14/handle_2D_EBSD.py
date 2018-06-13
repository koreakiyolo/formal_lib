#!/usr/bin/env python3
#!coding: utf-8


import pandas as pd
from pandas import DataFrame
import numpy as np
import os
import sys


def extract_df(target_df, x_y_colnms, range_dict):
    xcol, ycol = x_y_colnms
    c1 = target_df[x_col] >= range_dict.xmin 
    c2 = target_df[x_col] < range_dict.xmax
    c3 = target_df[y_col] >= range_dict.ymin
    c4 = target_df[y_col] < range_dict.ymax
    tmp = pd.concat([c1, c2, c3, c4], axis=1)
    total_c = np.min(tmp, axis=1)
    extracted_df = target_df[total_c]
    return extracted_df


def judge_columnar(ratio_ar, ratio=1.5):
    columnar = ratio_ar > ratio
    pass
