#!/usr/bin/env python
# !coding:utf-8

# formal lib
import numpy as np
from numpy import linalg as la
import copy
import sys
import os
import itertools

# my pythonlib
from create_poscar import POSCAR, change_coordinate_sys
from hexagonal import TwinInfo


def confirm_orthogonal_vecs(vecs, tolerance=1.0e-6):
    for a_vec, ano_vec in itertools.combinations(vecs, 2):
        va = np.dot(a_vec, ano_vec)
        if va > tolerance:
            sys.stderr.wirte("system is not\n")
            sys.exit(2)
    print("complete cofirming orthogonal system.\n")


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


def add_mirror_image(fposvecs, oneside_latvecs, twin_latvecs):
    # tvecs[0] and tvecs[1] is chosen as specular vecs.
    # you need to choose tvecs which apply to orthogonal set.
    # tvecs[2] is normal suface vec which is before normalization.
    # when cartesian vectors is converted to fractional vectors,
    # it is not "below 0 and over 1"
    cart_posvecs = np.dot(fposvecs, oneside_latvecs)
    surface_nvec = twin_latvecs[2] / la.norm(twin_latvecs[2])
    dists_from_surface = np.dot(cart_posvecs, surface_nvec)
    mirror_img = cart_posvecs - 2*dists_from_surface*surface_nvec
    mirror_img = copy.deepcopy(cart_posvecs)
    total_cposvecs = np.vstack([cart_posvecs, mirror_img])
    total_fposvecs = change_coordinate_sys(np.eye(3),
                                           total_cposvecs,
                                           twin_latvecs)
    total_fposvecs = total_fposvecs % 1.0
    return total_fposvecs


def add_mimage_act_onboudnary(fposvecs, oneside_latvecs,
                              twin_latvecs, fract_toler=1.0e-5):
    cpos_stack_li = []
    # fractional_vecs
    cond1 = fposvecs[:, 2] < fract_toler
    cond2 = fposvecs[:, 2] > 1.0 - fract_toler
    cond_onb = np.logical_or(cond1, cond2)
    if np.count_nonzero(cond_onb) == 0:
        print("any atoms are't on grainboundary(specular)")
    else:
        print("some atoms are on grainboundary(specular)")
    cond_notb = np.logical_not(cond_onb)
    notb_fposvecs = fposvecs[cond_notb]
    onb_fposvecs = fposvecs[cond_onb]
    # deal with not boundary position vectors
    notb_cposvecs = np.dot(notb_fposvecs, oneside_latvecs)
    surface_nvec = twin_latvecs[2] / la.norm(twin_latvecs[2])
    dists_from_surface = np.dot(notb_cposvecs, surface_nvec)
    mirror_img = notb_cposvecs - 2*dists_from_surface*surface_nvec
    cpos_stack_li.append(notb_cposvecs)
    cpos_stack_li.append(mirror_img)
    # deal with on boundary position vectors
    onb_fposvecs[:, 2] = 0
    added_onb_fpvecs = copy.deepcopy(onb_fposvecs)
    added_onb_fpvecs[:, 2] = 1.0
    cpos_stack_li.append(onb_fposvecs)
    cpos_stack_li.append(added_onb_fpvecs)
    # compile total posvecs
    total_cposvecs = np.vstack(cpos_stack_li)
    total_fposvecs = change_coordinate_sys(np.eye(3),
                                           total_cposvecs,
                                           twin_latvecs)
    total_fposvecs = total_fposvecs % 1.0
    return total_fposvecs


def get_poslayers_li(posvecs_cart, direction_cart,
                     tolerance=1.0e-5):
    # cartesian position vectors is divided into
    # layes accoring to direction
    # vectos.
    # return list with id of posvecs_cart
    normal_vec = direction_cart / la.norm(direction_cart)
    norm_ar_act_direct = np.dot(posvecs_cart, normal_vec)
    sorted_idar = np.argsort(norm_ar_act_direct)
    sorted_idli = sorted_idar.tolist()
    posid_ar = np.arange(len(posvecs_cart))
    processed_numli = []
    ans_li = []
    for one_id in sorted_idli:
        if one_id in processed_numli:
            continue
        tmp_ar = norm_ar_act_direct - norm_ar_act_direct[one_id]
        tmp_cond = tmp_ar < tolerance
        one_pair = posid_ar[tmp_cond]
        processed_numli.extend(one_pair.tolist())
        ans_li.append(one_pair)
    return ans_li


class GetLayersOfAxis(object):
    def __init__(self, fract_posvecs, latvecs, axis_num=2, tolerance=1.0e-5):
        # cartesian position vectors is divided into layes accoring to axis
        # direction vector.
        # return list with id of posvecs_cart
        # it can apply to the case when layer includes (0,0,0.001) fractinal
        # position and (0,0,0.9999) fractional position.
        # if tolerance is None, tolerance of fractional vectos is determined.
        axis_norm = la.norm(latvecs[axis_num])
        if tolerance is None:
            cart_tolerance = 1.0e-5
            fract_tolerance = cart_tolerance / axis_norm
        else:
            if not isinstance(float, tolerance):
                sys.stderr.write("you must enter float data into tolerance.\n")
                sys.exit(2)
            cart_tolerance = tolerance
            fract_tolerance = cart_tolerance / axis_norm
        axis_compo_ar = fract_posvecs[:, axis_num]
        processed_numli = []
        ans_li = []
        sorted_idar = np.argsort(fract_posvecs[:, axis_num])
        sorted_idli = sorted_idar.tolist()
        posid_ar = np.arange(len(fract_posvecs))
        for one_id in sorted_idli:
            if one_id in processed_numli:
                continue
            tmp_ar = axis_compo_ar - axis_compo_ar[one_id]
            tmp_cond = tmp_ar < fract_tolerance
            one_pair = posid_ar[tmp_cond]
            ans_li.append(one_pair)
            processed_numli.extend(one_pair.tolist())
        compo_cand1 = fract_posvecs[ans_li[0]][:, axis_num]
        compo_cand2 = fract_posvecs[ans_li[-1]][:, axis_num] - 1
        tmp_va = np.average(compo_cand1) - np.average(compo_cand2)
        new_ave = np.average(np.hstack((compo_cand1, compo_cand2)))
        if tmp_va < fract_tolerance:
            self.avelist = [new_ave]
            for a_pair in ans_li:
                layer_ave = np.average(fract_posvecs[a_pair][:, axis_num])
                self.avelist.append(layer_ave)
            ans_li[0].extend(ans_li[-1])
            ans_li = ans_li[:-1]
        else:
            self.avelist = []
            for a_pair in ans_li:
                layer_ave = np.average(fract_posvecs[a_pair][:, axis_num])
                self.avelist.append(layer_ave)
        self.ans_li = ans_li

    def __call__(self):
        return self.ans_li

    def get_layers_averaged_fpos(self):
        return self.avelist


def gene_translated_poslayers(fposvecs, layers_fpos_li,
                              boundary_cond=True, axis_num=2):
    # it translates position vectors according to an axis.
    # there are two translated types.
    # for example, first type makes a layer translate
    # to put it on boundary(0,0,1)
    # second type makes midpoint of two layers translate to put it on
    # boundary(0,0,1).
    # argument boundary_cond control such two types.
    # it returns generator whcih yield new and fractional
    # position vectors
    one_side_fpos = copy.deepcopy(fposvecs)
    if boundary_cond:
        for layer_pva in layers_fpos_li:
            gene_posvecs = copy.deepcopy(one_side_fpos)
            gene_posvecs[:, axis_num] = gene_posvecs[:, axis_num] - layer_pva
            gene_posvecs = gene_posvecs % 1
            yield gene_posvecs
    else:
        layers_fpos_li.sort()
        added_va = layers_fpos_li[0] + 1.0
        layers_fpos_li.append(added_va)
        layers_midpoint_pos_li = []
        for i in xrange(len(layers_fpos_li) - 1):
            mid_va = (layers_fpos_li[i] + layers_fpos_li[i + 1])/2.0
            layers_midpoint_pos_li.append(mid_va)
        for transrate_va in layers_midpoint_pos_li:
            gene_posvecs = copy.deepcopy(one_side_fpos)
            gene_posvecs[:, axis_num] = gene_posvecs[:, axis_num] - (
                                                        transrate_va
                                                                    )
            gene_posvecs = gene_posvecs % 1
            yield gene_posvecs


class PosTwinBase(POSCAR):
    # class instanceを用いて、自己複製を行わせる.
    # procedure
    # unit cell ===> matrix ====> translated matrix
    # ===> matrix and twin ====>
    def load_data(self, data=None):
        raise NotImplementedError

    def to_one_side_spcell(self):
        self.to_supercell_act_matrix_3_3(self.trnsform_mat)

    def to_twin_boudnary_model(self, tolerance=1.0e-5):
        new_latvecs = create_twinlatvecs(self.latvecs)
        elms_ar = copy.deepcopy(self.elements_array)
        uniq_elms_ar = np.unique(elms_ar)
        elms_stack_li = []
        fpos_stack_li = []
        for elm in uniq_elms_ar:
            cond = elms_ar == elm
            atom_cpos = self.cartesian_pos_vecs[cond]
            new_elms = elms_ar[cond]
            atom_total_fpos = add_mimage_act_onboudnary(
                                                    atom_cpos,
                                                    self.latvecs,
                                                    new_latvecs,
                                                    tolerance
                                                       )
            elms_stack_li.append(new_elms)
            fpos_stack_li.append(atom_total_fpos)
        total_fposvecs = np.vstack(fpos_stack_li)
        total_elms_ar = np.hstack(elms_stack_li)
        self.set_lat_vecs(new_latvecs)
        self.set_fposvecs_and_elmarray(total_fposvecs, total_elms_ar)

    def to_twindict(self):
        pos_dict = self.to_dict()
        pos_dict["twin_ins"] = copy.deepcopy(self.twin_ins)
        pos_dict["trnsform_mat"] = copy.deepcopy(self.trnsform_mat)
        return pos_dict

    def set_layers_index(self, tolerance=1.0e-5):
        layer_mi = GetLayersOfAxis(self.fractional_pos_vecs,
                                   self.latvecs,
                                   tolerance=1.0e-5)
        self.layers_li = layer_mi()
        self.layers_pos_li = layer_mi.get_layers_averaged_fpos()

    def gene_translated_matrixfpos(self, boundary_cond):
        oneside_fpos = copy.deepcopy(self.fractional_pos_vecs)
        gene = gene_translated_poslayers(oneside_fpos,
                                         self.layers_pos_li,
                                         boundary_cond)
        elms_ar = copy.deepcopy(self.elements_array)
        oneside_latvecs = copy.deepcopy(self.latvecs)
        for one_posvec in gene:
            self.set_fposvecs_and_elmarray(one_posvec, elms_ar)
            self.set_lat_vecs(oneside_latvecs)
            yield


class PosTwinFile(PosTwinBase):
    def __init__(self, pos_path, twin_file):
        self.load_data(pos_path, twin_file)

    def load_data(self, pos_path, twin_file):
        cond1 = os.path.exists(pos_path)
        cond2 = os.path.exists(twin_file)
        if not (cond1 and cond2):
            raise TypeError("file paths must be entered "
                            "which is related to poscar twin file.\n")
        POSCAR.__init__(self, pos_path)
        self.twin_ins = TwinInfo(twin_file)
        self.trnsform_mat = self.twin_ins.mat_act_hexalatvecs


class PosTwinDict(PosTwinBase):
    def __init__(self, twin_dict):
        self.load_data(twin_dict)

    def load_data(self, twindict):
        self.twin_ins = twindict.pop("twin_ins", None)
        self.trnsform_mat = twindict.pop("trnsform_mat", None)
        if isinstance(self.twin_ins, TwinInfo):
            ms = "twindict['twin_ins'] must has TwinInfo instance."
            sys.stderr.write(ms)
            sys.exit(2)
        elif isinstance(self.trnsform_mat, np.ndarray):
            ms = "twindict['trnsform_mat'] must has np.ndarray instance"
            sys.stderr.write(ms)
            sys.exit(2)
        POSCAR.__init__(self, twindict)


class PosTwin(PosTwinFile, PosTwinDict):
    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], dict):
            twindict = args[0]
            PosTwinDict.__init__(self, twindict)
        elif len(args) == 2:
            if os.path.exists(args[0]) and os.path.exists(args[1]):
                pospath = args[0]
                twinpath = args[1]
                PosTwinFile.__init__(self, pospath, twinpath)
            else:
                raise TypeError("poscar path or twin file path is not"
                                " appropriate")
        else:
            raise TypeError("args must be (1)dict instance or "
                            "(2)poscar path and twin info path.")

    @classmethod
    def duplicate_self(cls, twin_dict):
        return cls(twin_dict)
