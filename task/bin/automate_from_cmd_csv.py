#!/usr/bin/env python3

# formal lib
import argparse
from argparse import RawTextHelpFormatter
import os
# my lib
from help_gui import GUIHelper


def fnmstr(path_str):
    if not os.path.exists(path_str):
        mes = "{} is not file.".format(
                                    path_str
                                      )
        raise OSError(mes)
    return path_str


if __name__ == "__main__":
    msg = "this program helps"
    parser = argparse.ArgumentParser(
                                description=msg,
                                fromfile_prefix_chars="@",
                                formatter_class=RawTextHelpFormatter)
    parser.add_argument("csv", type=fnmstr, nargs="?")
    parser.add_argument("--wait_sec", type=int, nargs="?",
                        default=None)
    parser.add_argument("--off_input_wait",
                        action="store_false", default=True)
    args = parser.parse_args()
    CSV = args.csv
    WAIT_SEC = args.wait_sec
    OFF_INPUT_WAIT = args.off_input_wait
    gui_helper = GUIHelper(CSV)
    gui_helper.set_interval_input_cond(OFF_INPUT_WAIT)
    gui_helper.set_interval_waitsec(WAIT_SEC)
    gui_helper.run()
