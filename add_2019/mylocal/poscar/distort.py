#!/usr/bin/env python
# !coding:utf-8

# formal_lib
import numpy as np
from numpy import linalg as la
import sys
import os
import copy


# mylib
from . import POSCAR


def get_distortion_mat(distorted_latvecs, initial_latvecs):
    distortion_mat = np.dot(distorted_latvecs.T, initial_latvecs.T)
    return distortion_mat


class DistortPoscar(POSCAR):
    # this class can add some kinds of distortion to POSCAR.
    # at this time, fractional position vectors is unchanged.
    def __init__(self, poscar_path):
        self.initial_latvecs = None
        if os.path.exists(poscar_path):
            super(DistortPoscar, self).__init__(poscar_path)
            self.initial_latvecs = self.latvecs.copy()
        else:
            sys.stderr.write("poscar path is not appropriate.\n")
            sys.exit(2)

    def distort_self(self, distortion_mat):
        distorted_latvecs = np.dot(self.latvecs, distortion_mat)
        self.set_lat_vecs(distorted_latvecs)

    def gene_distort_poscar_gradually(self, one_side_step):
        initial_latvecs = copy.deepcopy(self.latvecs)
        avec = initial_latvecs[0]
        bvec = initial_latvecs[1]
        cvec = initial_latvecs[2]
        pl_vec = np.cross(avec, bvec)
        pl_norm_vec = pl_vec / la.norm(pl_vec)
        size = np.dot(cvec, pl_norm_vec)
        distortion_vec = (pl_norm_vec * size) - cvec
        step_ar = np.linspace(0, 2.0, one_side_step*2 + 1)
        for ratio in step_ar:
            new_cvec = cvec + ratio * distortion_vec
            new_latvecs = np.vstack([avec, bvec, new_cvec])
            self.set_lat_vecs(new_latvecs)
            print("set new lattice vectors")
            distort_mat = get_distortion_mat(new_latvecs,
                                             initial_latvecs)
            yield distort_mat

    def gene_get_gradual_distortion(self, latvecs, one_side_step):
        initial_latvecs = latvecs
        avec = initial_latvecs[0]
        bvec = initial_latvecs[1]
        cvec = initial_latvecs[2]
        pl_vec = np.cross(avec, bvec)
        pl_norm_vec = pl_vec / la.norm(pl_vec)
        size = np.dot(cvec, pl_norm_vec)
        distortion_vec = (pl_norm_vec * size) - cvec
        step_ar = np.linspace(0, 2.0, one_side_step*2 + 1)
        for ratio in step_ar:
            new_cvec = cvec + ratio * distortion_vec
            new_latvecs = np.vstack([avec, bvec, new_cvec])
            distort_mat = get_distortion_mat(new_latvecs,
                                             initial_latvecs)
            yield distort_mat

    def set_distortion_mat(self):
        distortion_mat = get_distortion_mat(self.latvecs,
                                            self.initial_latvecs)
        self.distort_mat = distortion_mat

    def generate_self(self):
        return copy.deepcopy(self)

    @classmethod
    def generate_DistortPos_from_dict(cls, pos_dict):
        return cls(pos_dict)


def get_mises_strain(distortion_mat):
    eta11 = distortion_mat[0][0]
    eta22 = distortion_mat[1][1]
    eta33 = distortion_mat[2][2]
    eta12 = distortion_mat[0][1]
    eta23 = distortion_mat[1][2]
    eta31 = distortion_mat[2][0]
    normal_comp = 1/6.0 * ((eta11 - eta22)**2 +
                           (eta22 - eta33)**2 +
                           (eta33 - eta11)**2)
    shear_comp = eta12**2 + eta23**2 + eta31**2
    mises_strain = np.sqrt(normal_comp + shear_comp)
    return mises_strain


def cnvt_strTomat(mat3_str):
    mat33 = np.array((float(va) for va in mat3_str()))
    mat33 = mat33.reshape(3, 3)
    return mat33


def cnvt_spcell_distortion_to_primtive(Tmat,
                                       distortion_mat):
    inv_trm = la.inv(Tmat)
    tmp = np.dot(inv_trm, distortion_mat)
    distortion_primitive = np.dot(tmp, Tmat)
    return distortion_primitive
