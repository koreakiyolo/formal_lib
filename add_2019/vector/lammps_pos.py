#!/usr/bin/env python3


import numpy as np
from abc import ABCMeta, abstractmethod
from numpy import linalg as la


MAIN_ATTRI_LIST = ["lattice", "Atoms", "Masses"]
SUB_ATTR_LIST = ["atoms", "atom types",
                 "xlo xhi", "ylo yhi", "zlo zhi", "xy xz yz"]


class LammpsPosBase(ABCMeta):
    @classmethod
    @abstractmethod
    def __init__(self):
        raise NotImplementedError("")

    def _confirm_base_attributions(self):
        pass

    def to_lammps(self, ofnm):
        pass
