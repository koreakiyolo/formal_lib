#!/usr/bin/env python3
# !coding:utf-8


import numpy as np
import os
import sys
import os
from collections import OrderedDict


class DivivdeLines(object):
    """
    """
    def __init__(self):
        """
        at first, it sets attributes.
        """
        self.double_bar_nums = []
        self.single_bar_nums = []
        self.va_bar_nums = []
        self.root_dict = OrderedDict()
        self.main_value_list = []
        self.cmts_li = []
        self.vas_li = []

    def reset_data(self):
        """
        it resrts attributes set at first
        """
        self.__init__()

    def load_file(self, micinput):
        """
        """
        with open(micinput, "r") as read:
            self.totlines = [a_line.strip() for a_line in read]
        for num, line in enumerate(self.totlines):
            if "# ===" in line[0:5]:
                self.double_bar_nums.append(num - 1)
            elif "# ---" in line[0:5]:
                self.single_bar_nums.append(num - 1)
            elif line[0] != "#":
                self.va_bar_nums.append(num)
            else:
                pass

    def divide_into_cmt_and_vas(self):
        """

        """
        ini_num = 0
        fin_va_num = len(self.va_bar_nums)
        for count, vl_num in enumerate(self.va_bar_nums):
            cmt = self.totlines[ini_num:vl_num]
            va = self.totlines[vl_num]
            ini_num = vl_num
            self.cmts_li.append(cmt)
            self.vas_li.append(va)
            if count == fin_va_num:
                try:
                    cmt = self.totlines[(vl_num + 1):]
                    self.cmts_li.append(cmt)
                except IndexError as e:
                    print("there is no comment line in the final lines")
                    break


    def write_mic_input(self, wpath, only_va=False):
        if type(only_va) is not bool:
            raise AttributeError
        if only_va:
            tmp = [st_va + "\n" for st_va in self.main_value_list]
        else:
            raise ImportError
        with open(wpath) as write:
            write.writelines(tmp)

