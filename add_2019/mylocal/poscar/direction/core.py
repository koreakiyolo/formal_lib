#!/usr/bin/env python
# !coding:utf-8

# formal lib
import sys
import os
import numpy as np
from numpy import linalg as la
import itertools

# my lib
from .. import POSCAR
from tool import calc_angle_directions_li


def get_nonequivalent_id(max_id=20):
    range_ar = np.arange(-(max_id - 1), max_id)
    gene_cand_id = itertools.combinations_with_replacement(range_ar, 3)
    tmp_candidate_set = set(gene_cand_id)
    tmp_candidate_set.discard((0, 0, 0))
    total_ar = np.vstack((one_id for one_id in tmp_candidate_set))
    return total_ar


class DirPos(POSCAR):
    # administer poscar data, primitive cell, and tranformation_matrix.
    # By using this object, you can extract direction index of primitive
    # cell as coordinate vectors of supercell system.
    # transform matrix is defined as follow.
    # (lattice vectors of supercell) = Tmatrix * (lattice vectors of unitcell)
    candidate_idar = None

    def __init__(self, pos_path, pprim_cell=None, trans_mat=None):
        # if prim_cell is None, pprim_cell = pos_path
        # when you set pprim_cell, you must input tranformation matrix.
        # transform matrix is defined as follow.
        if not os.path.exists(pos_path):
            sys.stderr.write("pos_path is invalid path.\n"
                             "error occurs in Dir_pos.__init__")
            sys.stderr.flush()
            sys.exit(2)
        super(DirPos, self).__init__(pos_path)
        if pprim_cell is None:
            print("pprim_cell is None.\n"
                  "this object regard the supercell as its' primitive cell.\n")
        else:
            if not os.path.exists(pprim_cell):
                sys.stderr.write("pprim_cell is invalid path.\n"
                                 "error occurs in Dirpos.__init__\n")
                sys.exit(2)
            elif trans_mat is None:
                sys.stderr.write("you must set tranformation matrix.\n"
                                 "program is terminated.")
                sys.exit(2)
            else:
                self.primpos_ins = POSCAR(pprim_cell)
                self.prim_latvecs = self.primpos_ins.latvecs
                if isinstance(trans_mat, np.ndarray):
                    self.trans_mat = trans_mat
                elif isinstance(trans_mat, list):
                    if len(trans_mat) == 9:
                        self.trans_mat = np.array(trans_mat).reshape(3, 3)
                else:
                    sys.stderr.write("unexpected input is "
                                     "set into trans_mat.\n")
                    sys.stderr.write("program is terminated.")
                    sys.exit(2)

    def get_direct_fromprim_tospcell(self, direct_id,
                                     integer_ratio=False):
        # this function convert direction based on primitive cell vectors to
        # direction based on supercell vectors.
        direct_act_splatvecs = np.dot(direct_id.reshape(1, 3),
                                      la.inv(self.trans_mat))
        if not integer_ratio:
            return direct_act_splatvecs
        else:
            if self.candidate_idar is None:
                self.candidate_idar = get_nonequivalent_id()
            base_direct = np.dot(direct_act_splatvecs, self.latvecs)
            candidate_dir_ar = np.dot(self.candidate_idar,
                                      self.latvecs)
            angle_ar = calc_angle_directions_li(
                                            base_direct,
                                            candidate_dir_ar
                                               )
            angledif_ar = np.abs(angle_ar)
            cond = np.argsort(angledif_ar)
            return (self.candidate_idar[cond], angledif_ar[cond])

    def get_pldirect_fromprim_tospcell(self, plane_id,
                                       integer_ratio=False):
        # this function convert plane-normal vector based on reciprocal
        # vectors of primitive cell to that based on reciprocal vectors of
        # supercell.
        prim_reciprocal_vecs = self.primpos_ins.reciprocal_vecs
        spcell_reciprocal_vecs = self.reciprocal_vecs
        inv_reciprocal_Tmat = np.dot(prim_reciprocal_vecs,
                                     la.inv(spcell_reciprocal_vecs))
        spcell_plane_id = np.dot(plane_id, inv_reciprocal_Tmat)
        if not integer_ratio:
            return spcell_plane_id
        else:
            if self.candidate_idar is None:
                self.candidate_idar = get_nonequivalent_id()
            base_direct = np.dot(spcell_plane_id, self.reciprocal_vecs)
            candidate_dir_ar = np.dot(self.candidate_idar,
                                      self.reciprocal_vecs)
            angle_ar = calc_angle_directions_li(
                                            base_direct,
                                            candidate_dir_ar
                                               )
            angledif_ar = np.abs(angle_ar)
            cond = np.argsort(angledif_ar)
            return (self.candidate_idar[cond], angledif_ar[cond])
