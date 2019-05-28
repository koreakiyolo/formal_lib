#!/usr/bin/env python
# !coding:utf-8

# formal_lib
import numpy as np
from numpy import linalg as la
import copy

# my_lib
from poscar import POSCAR
from poscar import calc_volume


class PosKpoint(POSCAR):
    def __init__(self, pos_fpath):
        POSCAR.__init__(self, pos_fpath)
        self.set_reciprocal_volume()
        self.set_sampling_ratio_from_norm()

    def set_reciprocal_volume(self):
        self.rec_volume = calc_volume(self.reciprocal_vecs)

    def set_sampling_ratio_from_norm(self):
        norm_ar = np.apply_along_axis(la.norm, 1,
                                      self.reciprocal_vecs)
        min_value = min(norm_ar)
        ratio_ar = norm_ar / min_value
        self.ratio_revecs_ar = ratio_ar


class Kpoints(object):
    def __init__(self, kp_file):
        self.load_kpoints(kp_file)

    def load_kpoints(self, kp_file):
        with open(kp_file) as read:
            read = open(kp_file, "r")
            read_text = [one_line.strip() for one_line
                         in read.readlines()]
        if (read_text[0] == "Automatic mesh") and (
            read_text[1] == "0"):
            first_two_lines = read_text[0:2]
            self.first_twoline_li = first_two_lines
        else:
            print("error occurs in kpoints file")
        mesh_method = read_text[2]
        if mesh_method.find("Gamma") >= 0:
            Gamma_line = read_text.index("Gamma")
            kmesh_num_ar = (
                            float(one_value) for one_value in
                            read_text[Gamma_line + 1].split()
                           )
            kmesh_num_ar = np.array(kmesh_num_ar)
            shift_of_kmesh = (
                              float(one_value) for one_value in
                              read_text[Gamma_line + 2].split()
                             )
            shift_of_kmesh = np.array(shift_of_kmesh)
        elif mesh_method.find("Monkhorst-Pack") >= 0:
            Monkhorst_line = read_text.index("Monkhorst-Pack")
            kmesh_num_ar = (
                            float(one_value) for one_value in
                            read_text[Monkhorst_line + 1].split()
                           )
            kmesh_num_ar = np.array(kmesh_num_ar)
            shift_of_kmesh = (
                              float(one_value) for one_value in
                              read_text[Monkhorst_line + 2].split()
                             )
            shift_of_kmesh = np.array(shift_of_kmesh)
        else:
            print("kpoints file is other.")
        self.kmesh_num_ar = kmesh_num_ar
        self.mesh_method = mesh_method
        self.shift_of_kmesh = shift_of_kmesh
        self.first_two_lines = first_two_lines
        self.total_knum = np.product(self.kmesh_num_ar)

    def write_kpoints(self, write_fpath="KPOINTS"):
        write_li = copy.deepcopy(self.first_twoline_li)
        write_li.append(self.mesh_method)
        # you must modify the following line.
        str_knum_li = (str(int(va)) for va in self.kmesh_num_ar)
        one_line_knum = " ".join(str_knum_li)
        write_li.append(one_line_knum)
        write_li = [one_line + "\n" for one_line in write_li]
        # you modify two blooks of with.
        with open(write_fpath, "w") as write:
            write.writelines(write_li)
            np.savetxt(write, self.shift_of_kmesh)


if __name__ == "__main__":
    import argparse
    msg = "this program makes KPOINTS file.\n"\
          "but the following part is incomplete.\n"
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument("--model_dir_path", "-m_dir",
                        type=str, nargs="?", required=True)
    parser.add_argument("--poscar_path", "-pos",
                        type=str, nargs="?",
                        required=True)
    parser.add_argument("--conditions", type=str,
                        nargs="?", default="all")
    parser.add_argument("--new_kmesh_method", "-kmethod",
                        type=str, nargs="?",
                        default="Monk_horst-Pack")
    parser.add_argument("--gamma", "-gmesh",
                        action="store_true", default=None)
    args = parser.parse_args()
    conditions = args.conditions
    new_kmesh_method = args.new_kmesh_method
    model_dir_path = args.model_dir_path
    if args.gamma:
        new_kmesh_method = "Gamma"

