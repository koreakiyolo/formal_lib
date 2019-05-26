#!/usr/bin/env python3

# formal lib
from pymatgen import MPRester
import itertools
import os


class MatProAPI(object):
    def __init__(self, API_key_file):
        with open(API_key_file) as read:
            self.API_KEY = read.readline().strip()

    def set_info_wfile(self, info_wfile):
        if os.path.exists(info_wfile):
            pass



file = open('feature.csv', 'w')
file.write('pretty_formula,volume,density,nsites,spacegroup,total_magnetization,formation_energy_per_atom,band_gap\n')

API_KEY = 'Your API-KEY' # Materials Project の API をここに入れる

# pymatgen は 103 元素扱えるので、binary は C(103,2) = 5253 パターンありえる
all_symbols = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr"]
allBinaries = itertools.combinations(all_symbols, 2) 

with MPRester(API_KEY) as m:
    for system in allBinaries:
        results = m.get_data(system[0] + '-' + system[1], data_type='vasp') # 計算データ（VASP）を入手
        for material in results:
            if material['e_above_hull'] < 1e-6: # 熱力学的安定性のチェック。凸包上にデータがあればその物質は安定（分解しない）。
                output = material['pretty_formula'] + ',' 
                       + str(material['volume']) + ',' 
                       + str(material['density']) + ',' 
                       + str(material['nsites']) + ',' 
                       + str(material['spacegroup']['number']) + ','
                       + str(material['total_magnetization']) + ','
                       + str(material['formation_energy_per_atom']) + ',' 
                       + str(material['band_gap'])
                file.write(output + '\n')

file.close()
