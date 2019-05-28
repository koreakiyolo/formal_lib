#!/usr/bin/env python
# !coding:utf-8

import numpy as np
import sys


class GetLayersOfAxis(object):
    def __init__(self, cart_pvecs, latvecs ,axis_num=2, tolerance=1.0e-1):
        """
        cartesian position vectors is divided into layes accoring to axis \
        vector.
        return list with id of posvecs_cart
        it can apply to the case when layer includes (0,0,0.001) fractinal
        position and (0,0,0.9999) fractional position.
        if tolerance is None, tolerance of fractional vectos is
        determined.
        """
        self.axis = axis_num
        self.latvecs = latvecs
        self.bool_crossed_layer = False
        if not isinstance(tolerance, float):
            sys.stderr.write("tolerance value is not float.\n")
            sys.exit(2)
        axis_compo_ar = cart_pvecs[:, axis_num]
        processed_numli = []
        ans_li = []
        sorted_idar = np.argsort(cart_pvecs[:, axis_num])
        sorted_idli = sorted_idar.tolist()
        posid_ar = np.arange(len(cart_pvecs))
        for one_id in sorted_idli:
            if one_id in processed_numli:
                continue
            tmp_ar = np.abs(axis_compo_ar - axis_compo_ar[one_id])
            tmp_cond = tmp_ar < tolerance
            one_pair = posid_ar[tmp_cond]
            ans_li.append(one_pair)
            processed_numli.extend(one_pair.tolist())
        compo_cand1 = cart_pvecs[ans_li[0]][:, axis_num]
        compo_cand2 = cart_pvecs[ans_li[-1]][:, axis_num] - 1
        tmp_va = np.average(compo_cand1) - np.average(compo_cand2)
        if np.abs(tmp_va) < tolerance:
            print("\n one layer crosses priodic boundary.\n")
            ans_li[0] = np.hstack((ans_li[0], ans_li[-1]))
            ans_li = ans_li[:-1]
        self.layers_idli = ans_li

    def convert_layercpos_ar(self, cart_pvecs):
        layercpos_li = []
        comp_pos = cart_pvecs[:, self.axis]
        for a_layer_li in self.layers_idli:
            layer_comp = comp_pos[a_layer_li]
            cond = layer_comp < 0
            translated_comp = layer_comp[cond] + self.latvecs[self.axis]
            cpos = np.average(np.hstack((layer_comp[~cond], translated_comp)))
            layercpos_li.append(cpos)
        return np.array(layercpos_li)

    def get_layers_li(self):
        return self.layers_idli
