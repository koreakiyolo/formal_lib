#!/usr/bin/env python
# !coding:utf-8

import subprocess
import os


def admin_subprocess(process_li, env=None):
    proc_li = []
    for one_process in process_li:
        proc = subprocess.Popen(one_process,
                                stdout=subprocess.PIPE,
                                env=env)
        proc_li.append(proc)
    output_li = []
    for a_proc in proc_li:
        output_li.append(a_proc.communicate())
    return output_li


def run_openssl():
    env = os.environ.copy()
    return env


def to_list(string):
    return string.split()


if __name__ == "__main__":
    import argparse
    message = "this program administrate subprocess "\
              "by starting new shell"
    parser = argparse.ArgumentParser(description=message,
                                     fromfile_prefix_chars="@")
    parser.add_argument("pos_process", type=to_list, nargs="*")
    args = parser.parse_args()
    process_li = args.pos_process
    output_li = admin_subprocess(process_li)
    print(output_li)
