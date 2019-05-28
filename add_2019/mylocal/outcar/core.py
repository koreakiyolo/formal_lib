#!/usr/bin/env python
# !coding:utf-8

import numpy as np
from pandas import DataFrame
import pickle

class Outcar_MD(object):
    def __init__(self,
                 outcar_path=None,
                 pos_and_force=False,
                 stress_tensor=False,
                 energy_df=True,
                 calc_time=True,
                 e_without=True):
        if outcar_path is None:
            return
        if pos_and_force:
            add_pos_force_sfn = Add_positions_and_forces()
        if stress_tensor:
            self.stress_tensor_li = []
        if energy_df:
            add_energy_sfn = Add_energy_info()
        if calc_time:
            self.calc_time_li = []
        if e_without:
            self.e_without_li = []
        with open(outcar_path, "r") as read:
            while True:
                try:
                    one_line = read.next()
                    if pos_and_force:
                        add_pos_force_sfn(one_line)
                    if stress_tensor:
                        self.add_stress_tensor(one_line)
                    if energy_df:
                        add_energy_sfn(one_line)
                    if calc_time:
                        self.add_calc_time(one_line)
                    if e_without:
                        self.add_e_without(one_line)
                except StopIteration:
                    break
        if pos_and_force:
            self.forces_li = add_pos_force_sfn.forces_li
            self.positions_li = add_pos_force_sfn.positions_li
        if energy_df:
            self.energy_info_df = add_energy_sfn.convert_df()

    def add_calc_time(self, one_line):
        if "LOOP+" in one_line:
            tmp_li = one_line.split()
            cputime = float(tmp_li[3][:-1])
            realtime = float(tmp_li[6])
            self.calc_time_li.append((cputime, realtime))

    def add_e_without(self, one_line):
        if "energy  without entropy" in one_line:
            en_without = float(one_line.split()[3])
            self.e_without_li.append(en_without)

    def add_stress_tensor(self, one_line):
        if "in kB" in one_line:
            tmp = np.array((float(num) for num in one_line.split()[1:]))
            self.stress_tensor_li.append(tmp)

    def serialize(self, file_name):
        with open(file_name ,"wb") as write:
            pickle.dump(self, write)


class Add_energy_info(object):
    def __init__(self):
        self.flag = False
        self.e_without_entropy_li = []
        self.ion_electron_TOTEN_li = []
        self.kinetic_e_li = []
        self.kinetic_lattice_li = []
        self.nose_potential_li = []
        self.nose_kinetic_li = []

    def __call__(self, one_line):
        if "ENERGY OF THE ELECTRON-ION-THERMOSTAT SYSTEM" in one_line:
            self.flag = True
        if self.flag:
            if "ion-electron   TOTEN" in one_line:
                ion_eTOTEN = float(one_line.split()[4])
                self.ion_electron_TOTEN_li.append(ion_eTOTEN)
            elif "kinetic energy EKIN" in one_line:
                kinetic_e = float(one_line.split()[4])
                self.kinetic_e_li.append(kinetic_e)
            elif "kin. lattice  EKIN_LAT=" in one_line:
                kinetic_lat = float(one_line.split()[3])
                self.kinetic_lattice_li.append(kinetic_lat)
            elif "nose potential ES" in one_line:
                nose_pote = float(one_line.split()[4])
                self.nose_potential_li.append(nose_pote)
            elif "nose kinetic" in one_line:
                nose_kine = float(one_line.split()[4])
                self.nose_kinetic_li.append(nose_kine)
                self.flag = False
            else:
                pass

    def convert_df(self):
        content_ar = np.array([self.ion_electron_TOTEN_li,
                               self.kinetic_e_li,
                               self.kinetic_lattice_li,
                               self.nose_potential_li,
                               self.nose_kinetic_li])
        columns_name = ["total_ion_energy", "kinetic_energy",
                        "lattice_kinetic", "nose_potential",
                        "nose_potential"]
        output_df = DataFrame(content_ar.T, columns=columns_name)
        return output_df


# substitute for statical variable:
class Add_positions_and_forces(object):
    def __init__(self):
        self.forces_li = []
        self.positions_li = []
        self.flag1 = False
        self.flag2 = False
        self.tmp_li = []

    def __call__(self, one_line):
        if "POSITION" in one_line and "TOTAL-FORCE" in one_line:
            self.flag1 = True
            return None
        if self.flag1:
            if "------------" in one_line:
                self.flag2 = True
                self.tmp_li = []
                return None
        elif self.flag1 and self.flag2:
            if "-----------" in one_line:
                self.flag1 = False
                self.flag2 = False
                step_data = np.vstack(self.tmp_li)
                force_data = step_data[:, 3:6]
                positions_data = step_data[:, 0:3]
                self.forces_li.append(force_data)
                self.positions_li.append(positions_data)
            one_atom = np.array([float(num) for num in one_line.split()])
            self.tmp_li.append(one_atom)

if __name__ == "__main__":
    # formal lib
    import argparse
    # my lib
    import support_arg
    message = "this program extract some information from OUTCAR of "\
              "MD and convert pickle file and csv fike"
    parser = argparse.ArgumentParser(description=message,
                                     fromfile_prefix_chars="@")
    parser.add_argument("--pickle_f", type=support_arg.wpath,
                        nargs="?",
                        default="OUTCAR.pickle")
    parser.add_argument("input_outcar",
                        type=support_arg.rpath,
                        nargs="?")
    parser.add_argument("--energy_csv", type=support_arg.wpath,
                        nargs="?", default="energy_info.csv")
    args = parser.parse_args()
    print(args)
    outcar_ins = Outcar_MD(args.input_outcar)
    outcar_ins.serialize(args.pickle_f)
    outcar_ins.energy_info_df.to_csv(args.energy_csv)
