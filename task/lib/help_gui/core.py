#!/usr/bin/env python3


import pyautogui
from pandas import Series
import pandas as pd
from more_itertools import consume
import time


class GUIHelper(object):
    def __init__(self, cmd_csv, gui_interval=0.1):
        self.cmd_df = pd.read_csv(cmd_csv, header=None)
        pyautogui.PAUSE = gui_interval
        self.set_interval_input_cond()
        self.set_interval_waitsec()

    def _initialize(self):
        print("initialize!!")
        input("waiting for pressing enter key")
        pyautogui.click()

    def set_interval_input_cond(self, on_off=True):
        assert isinstance(on_off, bool)
        self._interval_input_cond = on_off

    def set_interval_waitsec(self, wait_sec=None):
        cond1 = wait_sec is None
        cond2 = isinstance(wait_sec, int)
        assert cond1 or cond2
        self.wait_sec = wait_sec

    def run_from_row(self, row):
        assert isinstance(row, Series)
        for va in row.to_list():
            if va.startswith("#"):
                self.press_special_key(va)
            else:
                pyautogui.write("{}".format(va))
                pyautogui.press("tab")

    def press_special_key(self, key_string):
        assert key_string.startswith("#")
        key_string = key_string.lstrip("#")
        tmp_list = key_string.split("*")
        if len(tmp_list) == 1:
            key = tmp_list[0]
            self._check_special_key(key)
            pyautogui.press(key)
        elif len(tmp_list) == 2:
            key, num = tmp_list
            self._check_special_key(key)
            for i in range(int(num)):
                pyautogui.press(key)
        else:
            raise AssertionError("")

    def _check_special_key(self, key):
        assert key in pyautogui.KEYBOARD_KEYS

    def _coroutine_run(self):
        for _, row in self.cmd_df.iterrows():
            self._initialize()
            self.run_from_row(row)
            if self.set_interval_input_cond:
                input("waiting for enter key.")
            elif self.wait_sec is not None:
                time.sleep(self.wait_sec)
            yield

    def run(self):
        consume(self._coroutine_run())
