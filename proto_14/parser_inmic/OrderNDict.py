#!/usr/bin/env python3

from collections import OrderedDict


class OrderNDict(OrderedDict):
    def __init__(self, args):
        super(OrderNDict, self).__init__(args)
        self.key_li = []

    def _reset_apply_li(self):
        self.key_li = list(self.keys())

    def __getitem__(self, key):
        if type(key) == int:
            key = self.key_li[key]
            super(OrderNDict, self).__getitem__(key)
        elif type(key) == str:
            super(OrderNDict, self).__getitem__(key)
        else:
            raise KeyError("key must be object of int or str.")

    def __setitem__(self, key, new_va):
        if type(key) == int:
            try:
                key = self.key_li[key]
            except IndexError:
                print("key is unset")
                raise AttributeError
            super(OrderNDict, self).__setitem__(key, new_va)
        elif type(key) == str:
            super(OrderNDict, self).__setitem__(key, new_va)
        else:
            raise KeyError("key must be object of int or str.")
        self._reset_apply_li()

class
