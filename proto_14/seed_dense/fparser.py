#!/usr/bin/env python3
#!coding:utf-8

import argparse
from argparse import ArgumentParser

FUNC_TYPE_LI = ["EXPONENTIAL", "GAUSSIAN", "LORENTZIAN"]
"""
EXPONENTIAL f(x) = C*exp(-a*x)
GAUSSIAN f(x) = Cexp-a(x-b)**2
LORENTZIAN f(x) = unknown
"""


def confirm_functype(argstr):
    if type(argstr) != str:
        raise TypeError
    if argstr not in FUNC_TYPE_LI:
        raise ArgumentParser
    return argstr


class FuncInputGenerator():
    def __init__(self, AdminManyF_ins):
        msg = "this parser helps file convert seed density input"
        lparser = argparse.ArgumentParser(description=msg)
        lparser.add_argument("--functype", type=confirm_ftype,
                             nargs="?", required=True)
        lparser.add_argument("--C", type=float, nargs="?", default=1.0)
        lparser.add_argument("--a", type=float, nargs="?", required=True)
        lparser.add_argument("--b", type=float, nargs="?")
        self.lparser = lparser
        self.adminMfunc = AdminManyF_ins

    def add_linearg(self, a_line):
        args = a_line.split()
        line_args = self.lparser.parse_args(args)
        tmp_ftype = line_args.functype
        tmp_C = line_args.C
        tmp_a = line_args.a
        tmp_b = line_args.b
        if tmp_ftype == "EXPONENTIAL":
            pass
        elif tmp_ftype == "GAUSSIAN":
            pass
        elif tmp_ftype == "LORENTZIAN":
            pass


class Fparser(ArgumentParser):
    pass
