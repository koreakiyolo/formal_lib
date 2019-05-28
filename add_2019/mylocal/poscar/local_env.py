#!/usr/bin/env python
# !coding:utf-8

# formal_lib
import numpy as np
from numpy import linalg as la

# my_lib
from create_poscar import POSCAR


class PoscarForCEnv(POSCAR):

    def __init__(self, poscar_file, cutoff_dist=7):
        POSCAR.__init__(self, poscar_file)
        self._set_coordinate_environ_within_cutoff(cutoff_dist)

    def _set_coordinate_environ_within_cutoff(self, cutoff_dist,
                                              error_va=1.0e-6):
        self._set_probable_Tvecs(cutoff_dist)
        posvecs = self.cartesian_pos_vecs
        elms_array = self.elements_array
        stack_list = (posvecs + tvec for tvec in self.probable_Tvecs)
        total_posvecs = np.vstack(stack_list)
        stack_elm_list = [elms_array] * len(self.probable_Tvecs)
        total_elms = np.hstack(stack_elm_list)
        self.coodinate_env_pos_el_l = []
        self.coodinate_env_norm_el_l = []
        for a_pos in posvecs:
            probable_pvecs = total_posvecs - a_pos
            norm_info = np.apply_along_axis(la.norm,
                                            1,
                                            probable_pvecs.reshape(-1, 3))
            cond1 = norm_info <= cutoff_dist
            cond2 = norm_info >= error_va
            cond = np.logical_and(cond1, cond2)
            matched_norm = norm_info[cond]
            sort_cond = np.argsort(matched_norm)
            matched_pvecs = probable_pvecs[cond]
            matched_elms = total_elms[cond]
            sorted_pvecs = matched_pvecs[sort_cond]
            sorted_elms = matched_elms[sort_cond]
            sorted_norm = matched_norm[sort_cond]
            anspos = (sorted_pvecs, sorted_elms)
            ansnorm = (sorted_norm, sorted_elms)
            self.coodinate_env_pos_el_l.append(anspos)
            self.coodinate_env_norm_el_l.append(ansnorm)

    def _set_probable_Tvecs(self, cutoff_dist):
        lat_vecs = self.latvecs
        mx_dist_in_Ucell = self._get_mx_dist_in_Ucell()
        v_component_l = []
        for one_num in range(len(lat_vecs)):
            v_component = self._get_vertical_vec_component(
                                                    lat_vecs,
                                                    one_num)
            v_component_l.append(v_component)
        probable_enlarge_vects = self._get_probable_ratio_vecs(
                                                    cutoff_dist,
                                                    mx_dist_in_Ucell,
                                                    v_component_l)
        probable_Tvecs = np.dot(probable_enlarge_vects, self.latvecs)
        norm_info = np.apply_along_axis(la.norm, 1, probable_Tvecs)
        probable_Tvecs = probable_Tvecs[norm_info <= (mx_dist_in_Ucell + cutoff_dist)]
        self.probable_Tvecs = probable_Tvecs

    def _get_mx_dist_in_Ucell(self):
        cartesian_pvecs = self.cartesian_pos_vecs
        dif_pvecs_list = []
        for extract_num in range(len(cartesian_pvecs)):
            if (extract_num + 1) == len(cartesian_pvecs):
                break
            ref_vecs = cartesian_pvecs[extract_num]
            dif_pvecs = cartesian_pvecs[(extract_num + 1):] - ref_vecs
            dif_pvecs_list.append(dif_pvecs)
        dif_pvects_ar = np.vstack(dif_pvecs_list)
        norm_inf = np.apply_along_axis(la.norm, 1, dif_pvects_ar)
        max_dist = np.max(norm_inf)
        return max_dist

    def _get_vertical_vec_component(self, lvects, target_num):
        target_vec = lvects[target_num]
        cond = np.ones(len(lvects))
        cond[target_num] = 0
        cond = cond.astype(np.bool)
        ref_vecs = lvects[cond]
        vertical_vec = reduce(np.cross, ref_vecs)
        normal_vec = vertical_vec / la.norm(vertical_vec)
        vertical_vec_component = np.dot(target_vec, normal_vec)
        abs_vcomponent = np.abs(vertical_vec_component)
        return abs_vcomponent

    def _get_probable_ratio_vecs(self, cutoff_dist, max_dist,
                                 vertical_component_list):
        # for example(1,2,3) act lattice vectors
        v_compo_ar = np.array(vertical_component_list)
        ref_dist = max_dist + cutoff_dist
        enlarge_ratio = np.ceil(ref_dist / v_compo_ar)
        enlarge_ratio = enlarge_ratio.astype(np.int64)
        probable_enlarge_rat_l = []
        for a_num in range(-enlarge_ratio[0],
                           enlarge_ratio[0] + 1):
            for b_num in range(-enlarge_ratio[1],
                               enlarge_ratio[1] + 1):
                for c_num in range(-enlarge_ratio[2],
                                   enlarge_ratio[2] + 1):
                    prob_rvec = np.array([a_num, b_num, c_num])
                    probable_enlarge_rat_l.append(prob_rvec)
        prob_rvecs = np.vstack(probable_enlarge_rat_l)
        return prob_rvecs
