#!/usr/bin/env python3


import subprocess
import os
from argparse import RawTextHelpFormatter
import argparse

PIP_BASE_CMD = "pip3 install {}"


def fnmstr(path_str):
    if not os.path.exists(path_str):
        mes = "{} is not file.".format(
                                    path_str
                                      )
        raise OSError(mes)
    return path_str


if __name__ == "__main__":
    msg = "this program automatically pip3 install libraries"
    parser = argparse.ArgumentParser(
                             description=msg,
                             fromfile_prefix_chars="@",
                             formatter_class=RawTextHelpFormatter)
    parser.add_argument("lib_file", type=fnmstr, nargs="?")
    parser.add_argument("--stdout", type=str, nargs="?",
                        default="./pipinstll.out")
    parser.add_argument("--stderr", type=str, nargs="?",
                        default="./pipinstall.err")
    args = parser.parse_args()
    LIB_FILE = args.lib_file
    STDOUT = args.stdout
    STDERR = args.stderr
    ENV_DICT = os.environ.copy()
    with open(LIB_FILE, "r") as read:
        cmd_arg_list = [line.strip() for line in read]
    stdout_io = open(STDOUT, "wb")
    stderr_io = open(STDERR, "wb")
    for cmd_arg in cmd_arg_list:
        cmd = PIP_BASE_CMD.format(cmd_arg)
        popen_ins = subprocess.Popen(cmd, shell=True,
                                     env=ENV_DICT,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        stdout, stderr = popen_ins.communicate()
        if len(stderr) != 9:
            emes = "STD_ERR LIB : {}\n".format(cmd_arg)
            stderr_io.write(emes)
        else:
            mes = "downloaded lib : {}\n".format(cmd_arg)
            stdout_io.write(mes)
