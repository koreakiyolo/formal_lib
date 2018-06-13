#!/usr/bin/env python3


import numpy as np
from math import exp
import argparse


class SeedDensityRadius(object):
    def __init__(self, min_va, max_va, num):
        """
        argument value is distance(micron meter)
        """
        self.ranks = np.linspace(min_va, max_va, num)
        if min_va <= 0:
            raise AssertionError("you enter minus radius."
                                 "you must enter positive value into min_va")

    def set_caller(self, caller_ob):
        if not hasattr(caller_ob, "__call__"):
            raise AttributeError
        self.__call__ = caller_ob
        self.caller = caller_ob
        self._set_rank_vas()

    def _set_rank_vas(self):
        self.rank_vas = np.apply_along_axis(self.caller, self.ranks)

    def write_result(self, wpath):
        num = len(self.ranks)
        result = np.empty((num, 2))
        result[:, 0] = self.ranks
        result[:, 1] = self.rank_vas
        with open(wpath, "w") as write:
            write.write("# it contains seed density data in the following.")
            np.savetxt(wpath, result)
        print("completing writing file.")

    def standardize_total_density(self, standardized_va):
        dif = self.ranks[1] - self.ranks[0]
        total_va = np.sum(self.rank_vas) * dif
        ratio = standardized_va/ total_va
        self.rank_vas = self.rank_vas * ratio


class GaussCaller(objct):
    def __init__(self, a, b, C=1):
        self.param_info = ["gaussian",
                           "a = "+ str(a),
                           "b = "+ str(b),
                           "C = "+ str(C)]
        def caller(x):
            return C * exp(-a(x-b)**2)
        self.__call__ = caller


class DecExpCaller(object):
    def __init__(self, a, C=1):
        self.param_info = ["decexp",
                           "a = "+ str(a),
                           "C = "+ str(C)]
        def caller(x):
            return C * exp(-a*x) 
        self.__call__ = caller


class LorentzCaller(object):
    def __init__(self):
        raise ImportError


class AdminManyFuncs(object):
    def __init__(self):
        self.gaussian_call_li = []
        # C * exp-a(x-b)**2
        self.lorentz_call_li = []
        # unknown
        self.decexp_call_li = []
        # C * exp(-ax)

    def add_gaussian_caller(self, a, b, C=1):
        def new_caller(x):
            return C * exp(-a(x-b)**2)
        self.gaussian_call_li.append(new_caller)

    def reset_gaussian_callers(self):
        self.gaussian_call_li = []

    def add_lorentz_caller(self):
        raise ImportError

    def reset_lorentz_callers(self):
        self.lorntz_call_li = []

    def add_decexp_caller(self, a, C=1):
        def new_caller(x):
            return C * exp(-a*x)
        self.decexp_call_li.append(new_caller)

    def reset_decexp_callers(self):
        self.decexp_call_li = []

    def get_gene_caller(self):
        attri_li = dir(self)
        tmp = (nm for nm in attri_li if "call_li" in nm)
        for caller_li_attr in tmp:
            caller_li = getattr(self, caller_li_attr)
            for caller in caller_li:
                yield caller


if __name__ == "__main__":
    msg = "this program helps to input file applying to MICRESS seed "\
          "density model"
    parser = argparse.ArgumentParser(description=msg,
                                     fromfile_prefix_chars="@")
    parser.add_argument("--write_file")
    parser.add_argument("--infile_parse")
