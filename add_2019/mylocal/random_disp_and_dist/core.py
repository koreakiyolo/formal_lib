#!/usr/bin/env pytthon3

# my lib
from poscar import POSCAR
# formal lib
import numpy as np
import math
from math import sqrt
RANDOM_SEED1 = 32


class PoscarRandom(POSCAR):
    def add_normal_disp(self, disp, atomic_nums):
        """
        displament's unit is angstrorm.
        """
        cartesian_vecs = self.cartesian_pos_vecs
        disp / sqrt(3)
