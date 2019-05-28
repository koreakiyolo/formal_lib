#!/usr/bin/env python3


import numpy as np


def normalize_vec(vec):
    normalized_vec = vec / la.norm(vec)
    return normalized_vec


def get_norm_and_nvec(vec):
    norm = la.norm(vec)
    nvec = vec / norm
    return norm, nvec


def get_orthoonal_vec(target_vec, ref_vec):
    normalized_refvec= normalized_vec(ref_vec1)
    tmp_norm = np.dot(target_vec, normalized_refvec)
    orthogonal_vec = target_vec - tmp_norm * normalized_refvec
    return orthogonal_vec


def get_orthoonal_norm_and_nvec(target_vec, ref_vec):
    orthogonal_vec = get_orthoonal_vec(target_vec, ref_vec)
    norm, nvec = get_norm_and_nvec(orthogonal_vec)
    return norm, nvec


class Standardize3DCartesian(object):
    def __init__(self, lattice):
        self._set_lattice(lattice)
    
    def _set_lattice(self, lattice):
        if lattice.dim != 2:
            raise TypeError("")
        dim1, dim2 = lattice.shape
        if dim1 != 3 or dim2 !=3:
            raise TypeError("lattice vecs is invalid.")
        self.base_lattice = lattice
    
    def _set_new_latvecs(self):
        self.new_latvecs = np.eye(3)
        1d_nvec = normalized_vec(
                        self.base_lattice[0])
        1d_va = la.norm(self.base_lattice[0])
        self.new_latvecs[0][0] = 1d_va
        2d_norm, 2d_nvec = get_orthoonal_norm_and_nvec(
                                     self.new_latvecs[1],
                                     self.new_latvecs[0])
        2d_1comp = np.dot(self.new_latvecs[1], 1d_nvec)
        self.new_latvecs[1][0] = 2d_1comp
        self.new_latvecs[1][1] = 2d_2comp

