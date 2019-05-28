#!/usr/bin/env python
# !coding:utf-8

import numpy as np
from numpy import linalg as la
import sys
import copy
import os


def calc_volume(self, lattice_vecs):
    a_v = lattice_vecs[0]
    b_v = lattice_vecs[1]
    c_v = lattice_vecs[2]
    volume = np.abs(np.dot(c_v, np.cross(a_v, b_v)))
    return volume


def multiply_Ucell_into_spcell(Tvecs, pos_vecs, enlarge_ratioar):
    """
    get tuple including lattice vecs and fractional position vectors.
    supercell is made by enlarging each lttice vectors.
    """
    new_pos_vecs = pos_vecs / enlarge_ratioar
    x_ratio = enlarge_ratioar[0]
    y_ratio = enlarge_ratioar[1]
    z_ratio = enlarge_ratioar[2]
    stack_list = []
    for x_num in range(x_ratio):
        for y_num in range(y_ratio):
            for z_num in range(z_ratio):
                Trans_pvecs = np.array(
                    [x_num, y_num, z_num]).astype(np.float64)
                Trans_pvecs = Trans_pvecs / enlarge_ratioar
                one_posvec = new_pos_vecs + Trans_pvecs
                stack_list.append(one_posvec)
    posvecs_enlarged = np.vstack(stack_list)
    new_Tvecs = np.dot(np.diag(enlarge_ratioar), Tvecs)
    return [new_Tvecs, posvecs_enlarged]


def change_coordinate_sys(pre_base_vecs, pre_fposvecs, post_base_vecs):
    pre_cposvecs = np.dot(pre_fposvecs, pre_base_vecs)
    post_fposvecs = np.dot(pre_cposvecs, la.inv(post_base_vecs))
    return post_fposvecs


def translate_pos_into_Ucell(pos_vecs_fractional):
    pos_vecs_into_Ucell = pos_vecs_fractional % 1
    return pos_vecs_into_Ucell


def make_spcell_latvecs_and_posvecs(spcell_trfm_matr,
                                    lat_vecs_cartesian,
                                    pos_fvecs,
                                    error_va=1.0e-8):
    sufficient_latp = _get_sufficient_latpoint(
        spcell_trfm_matr)
    nece_and_suff_latp_act_spcell = _get_nece_and_suff_latp_act_spcell(
        sufficient_latp, spcell_trfm_matr,
        error_va)
    atom_point = change_coordinate_sys(np.eye(3), pos_fvecs, spcell_trfm_matr)
    stack_list = []
    for T_vec in nece_and_suff_latp_act_spcell:
        p_cloud = atom_point + T_vec
        stack_list.append(p_cloud)
    total_atom_point = np.vstack(stack_list)
    spcell_posvecs = translate_pos_into_Ucell(total_atom_point)
    spcell_latvecs = np.dot(spcell_trfm_matr, lat_vecs_cartesian)
    return (spcell_latvecs, spcell_posvecs)


def _get_sufficient_latpoint(spcell_trfm_matr):
    """
        supercell_trfm_matr has three row_vectors act basis_lattice vector
        sufficient lattice point is based on basis vector, for example (1,2,1)
    """
    if spcell_trfm_matr.shape[0] != 3:
        sys.stderr.write("couldn't transform coodinate sys.\n"
                         "error occurs in _get_sufficient_latpoint.\n")
        sys.exit(2)

    def div_array_into_nega_posi(one_array):
        dif = 1
        nega_conditions = one_array <= 0
        posi_conditions = ~nega_conditions
        negative_val = np.sum(one_array[nega_conditions])
        positive_val = np.sum(one_array[posi_conditions])
        return np.array([negative_val, positive_val + 1, dif])
    arrays_for_arange = np.apply_along_axis(div_array_into_nega_posi, 0,
                                            spcell_trfm_matr)
    range_array = [np.arange(*one_range)
                   for one_range in arrays_for_arange.T]
    xx, yy, zz = np.meshgrid(*range_array)
    sufficient_latpoint = np.vstack([xx.ravel(), yy.ravel(), zz.ravel()]).T
    if sufficient_latpoint.shape[1] != 3:
        sys.stderr.write("not appropriate shape for "
                         "sufficient lattice point\n")
        sys.exit(2)
    return sufficient_latpoint


def _get_nece_and_suff_latp_act_spcell(sufficient_latpoint,
                                       spvecs_act_Ucellvecs,
                                       error_va=1.0e-8):
    suff_latvecs_act_spvecs = change_coordinate_sys(
                                np.eye(3), sufficient_latpoint,
                                spvecs_act_Ucellvecs
                                                   )
    one_conditinos = suff_latvecs_act_spvecs <= (1.0 - error_va)
    ano_conditions = suff_latvecs_act_spvecs >= (0 - error_va)
    total_conditions = np.logical_and(one_conditinos, ano_conditions)
    nece_and_suff_cond = np.apply_along_axis(
                                np.min, 1, total_conditions
                                            )
    nece_and_suff_latpoint_act_spcell = suff_latvecs_act_spvecs[
                                                    nece_and_suff_cond
                                                               ]
    return nece_and_suff_latpoint_act_spcell


class PosBase(object):

    def load_data(self, data=None):
        raise NotImplementedError

    def _set_additional_info(self):
        self._set_element_list_and_natom_list()
        self._set_element_and_num_dict()
        self._set_cartesian_pos_vecs()
        self._set_reciprocal_vectors()
        self._set_density_peratom()
        self._rearange_fpos_elm()
        self.change_into_rhanded_sys()

    # the following attribute can be only got and can't be set
    @property
    def norm(self):
        return self.__norm

    @property
    def fractional_pos_vecs(self):
        return self.__fractional_pos_vecs

    @property
    def element_list(self):
        return self.__element_list

    @property
    def natom_list(self):
        return self.__num_atom_list

    @property
    def elements_array(self):
        return self.__elements_array

    # the following attribute can be set and get.
    # it is mainly rewriten by especial method.
    @property
    def latvecs(self):
        return self.__lat_vecs

    @latvecs.setter
    def latvecs(self, new_lattice):
        self.set_lat_vecs(new_lattice)

    def set_lat_vecs(self, new_lattice):
        # it's a especial method to rewrite self.latvecs.
        # update main info.
        self.__lat_vecs = new_lattice
        # update additional info.
        self._set_additional_info()

    def set_fposvecs_and_elmarray(self, new_fposvecs, elmarray):
        if len(new_fposvecs) != len(elmarray):
            sys.stderr.write("can't rewrite posvecs and element information "
                             "because of unmached length.\n")
            sys.exit(2)
        new_pos, new_elm = self._help_arange_fpos_nelmar(new_fposvecs,
                                                         elmarray)
        pos_within_Ucell = translate_pos_into_Ucell(new_pos)
        self.__elements_array = new_elm
        self.__fractional_pos_vecs = pos_within_Ucell

    # some sub attributes are made by internal methods.
    def _set_element_list_and_natom_list(self):
        # indirectly update natom_list and element_list
        # by using elements_array
        elm_set = np.unique(self.__elements_array)
        self.__element_list = list(elm_set)
        tmp_list = []
        for a_elm in self.__element_list:
            cond = self.__elements_array == a_elm
            natom = np.count_nonzero(cond)
            tmp_list.append(natom)
        self.__num_atom_list = tmp_list

    def _rearange_fpos_elm(self):
        # arange given elm_array for example ["Ti", "O", "O", "Ti"]
        # into ["Ti", "Ti", "O", "O"] according to fracrional
        # posvecs order
        fpos = self.__fractional_pos_vecs
        elm_ar = self.__elements_array
        n_fpos, n_elm_ar = self._help_arange_fpos_nelmar(fpos, elm_ar)
        self.set_fposvecs_and_elmarray(n_fpos, n_elm_ar)

    def _help_rearange_fpos_nelmar(self, fposvecs, nelms_ar):
        elmset = np.unique(nelms_ar)
        pos_stack_li = []
        elm_stack_li = []
        for el in elmset:
            cond = nelms_ar == el
            one_elm_ar = nelms_ar[cond]
            one_elm_posvecs = fposvecs[cond]
            elm_stack_li.append(one_elm_ar)
            pos_stack_li.append(one_elm_posvecs)
        new_posvecs = np.vstack(pos_stack_li)
        new_elmvecs = np.hstack(elm_stack_li)
        return (new_posvecs, new_elmvecs)

    def _set_element_and_num_dict(self):
        self.element_and_num_dict = dict(
            zip(self.__element_list, self.__num_atom_list))

    def _set_cartesian_pos_vecs(self):
        cartesian_pos_vecs = np.dot(
                             self.__fractional_pos_vecs,
                             self.__lat_vecs)
        self.cartesian_pos_vecs = cartesian_pos_vecs

    def _set_reciprocal_vectors(self):
        practical_latvecs = self.__lat_vecs
        a_vec = practical_latvecs[0]
        b_vec = practical_latvecs[1]
        c_vec = practical_latvecs[2]
        volume = self.calc_volume(practical_latvecs)
        reciprocal_avec = np.cross(b_vec, c_vec) / volume
        reciprocal_bvec = np.cross(c_vec, a_vec) / volume
        reciprocal_cvec = np.cross(a_vec, b_vec) / volume
        reciprocal_vecs = np.vstack((reciprocal_avec,
                                     reciprocal_bvec,
                                     reciprocal_cvec))
        self.reciprocal_vecs = reciprocal_vecs

    def _set_density_peratom(self):
        self._help_set_actual_volume()
        print(self.element_and_num_dict)
        total_atom = sum(self.element_and_num_dict.values())
        self.density_peratom = total_atom / float(self.volume)

    def _help_set_actual_volume(self):
        volume = calc_volume(self.__lat_vecs)
        self.volume = volume

    # the following methods operate latvecs
    def change_into_rhanded_sys(self):
        if la.det(self.__lat_vecs) > 0:
            pass
        elif la.det(self.lattice_vectors_act_cartesian_without_norm) < 0:
            rhanded_lat = np.vstack(
                [self.__lat_vecs[0:2], -self.__lat_vecs[2]])
            self.set_lat_vecs(rhanded_lat)
            print("convert lattice_vectors to right handed sys")

    def cnvt_latvecs_in_easiest_way(self):
        latvecs = self.latvecs
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
        self.set_lat_vecs(new_latvecs)

    def change_POSCAR_coordinate_sys(self, new_cartesian_latvecs):
        old_cartesian_latves = self.__lat_vecs
        self.set_lat_vecs(new_cartesian_latvecs)
        new_posvecs = change_coordinate_sys(old_cartesian_latves,
                                            self.__fractional_pos_vecs,
                                            new_cartesian_latvecs)
        self.set_fposvecs_and_elmarray(new_posvecs,
                                       self.__elements_array)
        print("can convert only coordinate sys. can't make supercell.")

    # the following methods operates to convert primitive cell
    # in to supercell.
    def to_supercell_act_matrix_3_3(self, spcell_trfm_mat, error_va=1.0e-6):
        model_elm_ar = copy.deepcopy(self.elements_array)
        unique_elm_ar = np.unique(model_elm_ar)

        def trfm_unitcell(atom_fpvecs):
            return make_spcell_latvecs_and_posvecs(spcell_trfm_mat,
                                                   self.latvecs,
                                                   atom_fpvecs,
                                                   error_va)
        elms_stack_li = []
        fpos_stack_li = []
        for elm in unique_elm_ar:
            cond = model_elm_ar == elm
            atom_fpos = self.fractional_pos_vecs[cond]
            elms_ar = model_elm_ar[cond]
            splatvecs, sp_fposvecs = trfm_unitcell(atom_fpos)
            elms_stack_li.append(elms_ar)
            fpos_stack_li.append(sp_fposvecs)
        new_elms_ar = np.hstack(elms_stack_li)
        new_fposvecs = np.vstacK(fpos_stack_li)
        new_latvecs = splatvecs
        self.set_lat_vecs(new_latvecs)
        self.set_fposvecs_and_elmarray(new_fposvecs, new_elms_ar)

    def to_supercell_each_axis(self, enlarge_ratio):
        model_elm_ar = copy.deepcopy(self.elements_array)
        unique_elm_ar = np.unique(model_elm_ar)

        def enlarge_unitcell(atom_fpvecs):
            return multiply_Ucell_into_spcell(self.latvecs,
                                              self.atom_fpvecs,
                                              enlarge_ratio)
        elms_stack_li = []
        fpos_stack_li = []
        for elm in unique_elm_ar:
            cond = model_elm_ar == elm
            atom_fpos = self.fractional_pos_vecs[cond]
            elms_ar = model_elm_ar[cond]
            splatvecs, sp_fposvecs = enlarge_unitcell(atom_fpos)
            elms_stack_li.append(elms_ar)
            fpos_stack_li.append(sp_fposvecs)
        new_elms_ar = np.hstack(elms_stack_li)
        new_fposvecs = np.vstacK(fpos_stack_li)
        new_latvecs = splatvecs
        self.set_lat_vecs(new_latvecs)
        self.set_fposvecs_and_elmarray(new_fposvecs, new_elms_ar)

    # basical moethod of Poscar instance in the following.
    def write_to_poscar(self, POSCAR_file="POSCAR"):
        with open(POSCAR_file, "w") as write:
            write_list = []
            write_list.append(self.__compound)
            write_list.append(repr(self.__norm))
            write_list = [one_line + "\n" for one_line in write_list]
            write.writelines(write_list)
        with open(POSCAR_file, "a") as add:
            if la.det(self.__lat_vecs) > 0:
                np.savetxt(add, self.__lat_vecs)
            elif la.det(self.latvecs) < 0:
                right_handed_lattice = np.vstack(
                    [self.__lat_vecs[0:2], -self.__lat_vecs[2]])
                np.savetxt(add, right_handed_lattice)
            else:
                sys.stderr.write("determinant error!\n")
                sys.stderr.write("basis vectors don't make "
                                 "3 dimentions")
        with open(POSCAR_file, "a") as add2:
            elements_line = " ".join(self.__element_list)
            str_natom_list = [str(num) for num in self.__num_atom_list]
            elements_num_line = " ".join(str_natom_list)
            write_info = [elements_line, elements_num_line, "Direct"]
            add2_txt = [one_line + "\n" for one_line in write_info]
            add2.writelines(add2_txt)
        with open(POSCAR_file, "a") as add3:
            np.savetxt(add3, self.__fractional_pos_vecs)
        print("complete writing into " + POSCAR_file)

    def to_dict(self):
        new_dict = {}
        new_dict["comopound_name"] = copy.deepcopy(self.__compound)
        new_dict["norm"] = 1.0
        new_dict["lat_vecs"] = copy.deepcopy(self.latvecs)
        new_dict["element_list"] = copy.deepcopy(self.element_list)
        new_dict["num_atom_list"] = copy.deepcopy(self.natom_list)
        new_dict["fractional_pos_vecs"] = copy.deepcopy(
                                            self.fractional_pos_vecs
                                                       )
        return new_dict


class PosFile(PosBase):
    def __init__(self, input_data):
        self.load_data(input_data)

    def load_data(self, poscar_file=None):
        if not os.path.exists(poscar_file):
            sys.stderr.write("POSCAR_information has not entered.\n")
            sys.exit(2)
        with open(poscar_file, "r") as read:
            read_info = read.readlines()
        POSCAR_info = [one_line.strip() for one_line in read_info]
        compound_name = POSCAR_info[0]
        norm = float(POSCAR_info[1])
        latvecs_without_norm = np.loadtxt(POSCAR_info[2:5])
        element_list = POSCAR_info[5].split()
        natom_list = [int(num) for num in (POSCAR_info[6]).split()]
        total_atoms = sum(natom_list)
        point_num = POSCAR_info.index("Direct")
        fractional_pos_vecs = np.loadtxt(
            POSCAR_info[(point_num + 1):(point_num + 1 + total_atoms)])
        # basical poscar information
        self.__compound = compound_name
        self.__norm = 1.0
        self.__lat_vecs = latvecs_without_norm * norm
        self.__fractional_pos_vecs = fractional_pos_vecs
        self.__element_list = element_list
        self.__num_atom_list = natom_list
        # main information for element and positions
        tmp_nelms_li = []
        for n, el in zip(natom_list, element_list):
            nelement_l = n * [el]
            tmp_nelms_li.extend(nelement_l)
        self.__elements_array = np.array(tmp_nelms_li)
        # additional information
        self._set_additional_info()


class PosDict(PosBase):
    """
    you must enter the following information
    # (1)compound_name
    # (2)norm
    # (3)lat_vecs
    # (4)element_list
    # (5)num_atom_list
    """
    def __init__(self, load_data):
        self.load_data(load_data)

    def load_data(self, input_dict):
        if not isinstance(input_dict, dict):
            sys.stderr.write("POSCAR_information has not entered.\n")
            sys.exit(2)
        compound_name = input_dict.pop("compound_name", None)
        norm = input_dict.pop("norm", None)
        lat_vecs = input_dict.pop("lat_vecs", None)
        element_list = input_dict.pop("element_list", None)
        natom_list = input_dict.pop("num_atom_list", None)
        fractional_pos_vecs = input_dict("fractional_pos_vecs", None)
        if not isinstance(compound_name, str):
            sys.stderr.write("you must enter str data into key compound_name")
            sys.exit(2)
        if not isinstance(norm, float):
            sys.stderr.write("you must enter float data into key norm")
            sys.exit(2)
        if not isinstance(lat_vecs, np.ndarray):
            sys.stderr.write("you must enter np.ndarray data into "
                             "key lat_vecs")
            sys.exit(2)
        if not isinstance(element_list, list):
            sys.stderr.write("you must enter np.ndarray data into key"
                             " element_list")
            sys.exit(2)
        if not isinstance(natom_list, list):
            sys.stderr.write("you must enter np.ndarray data into key"
                             " num_atom_list")
            sys.exit(2)
        if not isinstance(fractional_pos_vecs, np.ndarray):
            sys.stderr.write("you must enter np.ndarray data into key"
                             " fractional_pos_vecs")
            sys.exit(2)
        if not len(fractional_pos_vecs) == np.sum(natom_list):
            ms = "fractional_pos_vecs length don't match number of atom.\n"
            sys.stderr.write(ms)
            sys.exit(2)
        if input_dict:
            raise TypeError("Unexpected input_dict: %r" % input_dict)
        # basical poscar information
        self.__compound = compound_name
        self.__norm = 1.0
        self.__lat_vecs = lat_vecs * norm
        self.__fractional_pos_vecs = fractional_pos_vecs
        self.__element_list = element_list
        self.__num_atom_list = natom_list
        # main information for element and positions
        tmp_nelms_li = []
        for n, el in zip(natom_list, element_list):
            nelement_l = n * [el]
            tmp_nelms_li.extend(nelement_l)
        self.__elements_array = np.array(tmp_nelms_li)
        # additional information
        self._set_additional_info()


class POSCAR(PosFile, PosDict):
    def __init__(self, input_data):
        if isinstance(input_data, str):
            PosFile.__init__(self, input_data)
        elif isinstance(input_data, dict):
            PosDict.__init__(self, input_data)
        else:
            raise TypeError("Unexpected input data of POSCAR class")
