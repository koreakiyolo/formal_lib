#!/usr/bin/env python
# !coding:utf-8

# formal lib
import numpy as np
from numpy import linalg as la
import itertools
import copy

# my pythonlib
from poscar_with_direction import DirPos
from make_twin import PosTwin


def calc_volume(vecs):
    pl_vec = np.cross(vecs[0], vecs[1])
    volume = la.norm(np.dot(pl_vec, vecs[2]))
    return volume


def get_reciprocal_vecs(actual_vecs):
    a_vec = actual_vecs[0]
    b_vec = actual_vecs[1]
    c_vec = actual_vecs[2]
    volume = calc_volume(actual_vecs)
    reciprocal_avec = np.cross(b_vec, c_vec) / volume
    reciprocal_bvec = np.cross(c_vec, a_vec) / volume
    reciprocal_cvec = np.cross(a_vec, b_vec) / volume
    reciprocal_vecs = np.vstack((reciprocal_avec,
                                 reciprocal_bvec,
                                 reciprocal_cvec))
    return reciprocal_vecs


def create_twinlatvecs(latvecs):
    a_vec = latvecs[0]
    b_vec = latvecs[1]
    c_vec = latvecs[2]
    pl_vec = np.cross(a_vec, b_vec)
    pl_nvec = pl_vec / la.norm(pl_vec)
    norm = np.dot(c_vec, pl_nvec)
    new_cvec = norm * pl_nvec
    new_latvecs = np.vstack((a_vec, b_vec, new_cvec))
    return new_latvecs


def trfm_simplest_coordinate_sys(latvecs):
    a_vec = latvecs[0]
    b_vec = latvecs[1]
    c_vec = latvecs[2]
    new_latvecs = np.zeros((3, 3))
    new_latvecs[0][0] = np.array([la.norm(a_vec), 0, 0])
    base_vec0 = a_vec / new_latvecs[0][0]
    new_latvecs[1][0] = np.dot(base_vec0, b_vec)
    new_latvecs[1][1] = la.norm(b_vec - (new_latvecs[1][0] * base_vec0))
    base_vec1 = b_vec / la.norm(new_latvecs[1])
    new_latvecs[2][0] = np.dot(base_vec0, c_vec)
    new_latvecs[2][1] = np.dot(base_vec1, c_vec)
    tmp_va_for_compo = c_vec - (new_latvecs[2][0]*base_vec0) - (
                                new_latvecs[2][1]*base_vec1)
    new_latvecs[2][2] = la.norm(tmp_va_for_compo)
    if la.det(new_latvecs) < 0:
        new_latvecs[2] = -new_latvecs[2]
    return new_latvecs


class PosTwinDir(PosTwin):
    # transformation matrix T(Twin) which convert one side
    # crystal to twin model.
    # transformation matrix T(sp) which convert primitive
    # cell to supercell.
    # they're defined in the following.
    # twin latvecs = T(Twin) * supercell
    # supercell = T(sp) * primitive cell
    def __init__(self, pcell_path, twin_fpath):
        super(PosTwinDir, self).__init__(pcell_path, twin_fpath)
        self.ini_latvecs = copy.deepcopy(self.latvecs)
        self.totally_process()

    def totally_preprocess(self):
        self.preprocess_pldirections()
        self.preprocess_directions()

    def totally_process(self):
        self.to_one_side_spcell()
        self.set_layers_index()
        boundary_gene = self.gene_traslated_matrixfpos(True)
        non_boundary_gene = self.gene_traslated_matrixfpos(False) 
        self.to_twin_boudnary_model()

    def preprocess_directions(self):
        oneside_latvcs = np.dot(self.trnsform_mat, self.ini_latvecs)
        oneside_latvcs = trfm_simplest_coordinate_sys(oneside_latvcs)
        twin_latvecs = create_twinlatvecs(oneside_latvcs)
        twin_latvecs = trfm_simplest_coordinate_sys(twin_latvecs)
        twin_Tmat = np.dot(twin_latvecs, la.inv(oneside_latvcs))
        directions_right_Tmat = la.inv(np.dot(
                                        twin_Tmat,
                                        self.trans_mat
                                             ))
        self.dir_right_Tmat = directions_right_Tmat
    
    def preprocess_pldirections(self):
        # transformation matrix rT(sp) which convert primitive
        pcell_recvecs = get_reciprocal_vecs(self.latvecs)
        onesd_latvecs = np.dot(self.trnsform_mat, self.ini_latvecs)
        onesd_recvecs = get_reciprocal_vecs(onesd_latvecs)
        recTmat_sp = np.dot(oneside_recvecs, la.inv(pcell_recvecs))
        onesd_latvecs = change_coordinate_sys(oneside_latvcs)
        onesd_recvecs = get_reciprocal_vecs(oneside_latvcs)
        twin_latvecs = create_twinlatvecs(oneside_latvcs)
        twin_latvecs = change_coordinate_sys(twin_latvecs)
        twin_recvecs = get_reciprocal_vecs(twin_latvecs)
        recTmat_twin = np.dot(twin_recvecs, la.inv(oneside_recvecs))
        pldir_right_Tmat = la.inv(np.dot(
                                    recTmat_twin,
                                    recTmat_sp
                                        ))
        self.pldir_right_Tmat = pldir_right_Tmat
         
    def make_mirror_id(self, id3_ar):
        new_id3 = copy.deepcopy(id3_ar)
        new_id3[2] = -new_id3[2]
        return new_id3

    def cnvt_pcell_direction(self, direct_3ar):
        return np.dot(direct_3ar, self.dir_right_Tmat)

    def cnvt_pcell_pldirection(self, pldirect_3ar):
        return np.dot(pldirect_3ar, self.pldir_right_Tmat)

    def cnvt_pcell_directions(self, directs_n3_ar):
        print("return multi directions n_3_matrix")
        return np.dot(directs_n3_ar, self.dir_right_Tmat)

    def cnvt_pcell_pldirections(self, pldirects_n3_ar):
        print("return multi plane directions n_3_matrix")
        return np.dot(directs_n3_ar, self.dir_right_Tmat)
