#!/usr/bin/env python3


# formal lib
from subprocess import Popen
from subprocess import SubprocessError
import os
import argparse
from argparse import RawTextHelpFormatter
import shutil
# my lib
PIP_INSTALL_BASECMD = "pip install {}"


def write_list(string_list, wfpath):
    with open(wfpath, "w") as write:
        for string in string_list:
            write.write(string + "\n")


def confirm_cmd(cmd):
    if shutil.which(cmd) is None:
        raise TypeError("cmdisn't exisiting.")


def confirm_subprocess_error(popen_ins):
    if not isinstance(popen_ins, Popen):
        raise AttributeError("open_ins isn't Popen instance.")
    if popen_ins.poll() != 0:
        emes = "while installing packages, subprocess error occurs."
        raise SubprocessError(emes)


def eliminate_version_info(package):
    latest_package = package.split("==")[0]
    return latest_package


if __name__ == "__main__":
    msg = "this program force pip install every package from files."
    parser = argparse.ArgumentParser(
                                  description=msg,
                                  formatter_class=RawTextHelpFormatter,
                                  fromfile_prefix_chars="@")
    parser.add_argument("packages", type=str, nargs="*")
    parser.add_argument("--elim_version", action="store_true",
                        default=False)
    parser.add_argument("--error_log", type=str, nargs="?",
                        default="./error_pckg.txt")
    args = parser.parse_args()
    PACKAGES = args.packages
    ELIM_VERSION = args.elim_version
    ERROR_LOG = args.error_log
    ENV_DICT = os.environ.copy()
    errors_packages = []
    confirm_cmd("pip")
    for pckg in PACKAGES:
        cmd_pip = PIP_INSTALL_BASECMD.format(pckg)
        if ELIM_VERSION:
            cmd_pip = eliminate_version_info(cmd_pip)
        popen_ins = Popen(cmd_pip, shell=True,
                          env=ENV_DICT, cwd=os.getcwd())
        popen_ins.communicate()
        try:
            confirm_subprocess_error(popen_ins)
        except SubprocessError:
            errors_packages.append(pckg)
    write_list(errors_packages, ERROR_LOG)
