#!/usr/bin/env python
# !coding:utf-8

import os
import sys


HOME = os.getenv("HOME")
zshrc = os.path.join(HOME, ".zshrc")


def get_env_variable(env_nm="PATH"):
    string_va = os.getenv(env_nm)
    if string_va is None:
        sys.stderr.write("enviroment value is unknown.\n")
        sys.exit(2)
    va_path_li = string_va.split(":")
    path_li = [i for i in va_path_li if i != ""]
    return path_li


def confirm_path_exists(paths_li):
    new_paths = [a_path for a_path in paths_li
                 if os.path.exists(a_path)]
    return new_paths


def set_env_path(new_paths):
    if not new_paths:
        sys.stderr.write("all path is not existing.\n")
        sys.exit(2)
    env_va = ":".join(new_paths)
    return env_va


def write_env_file(env_nm, env_va, set_file="zshrc"):
    msg = "\n"
    msg += "export " + env_nm + "=" + env_va + "\n"
    with open(set_file, "a") as write:
        write.write(msg)

if __name__ == "__main__":
    import argparse
    msg = "this program help set approproiate path and "\
          "delete not existing path.\n"
    parser = argparse.ArgumentParser(description=msg,
                                     fromfile_prefix_chars="@")
    parser.add_argument("--env_nm", nargs="?", type=str,
                        required=True)
    parser.add_argument("--zshrc", action="store_true",
                        default=True)
    parser.add_argument("--bashrc",
                        default=False, action="store_true")
    parser.add_argument("--add", default=False, nargs="?", type=str)
    parser.add_argument("--delete", type=str, nargs="?",
                        default=False)
    args = parser.parse_args()
    env_nm = args.env_nm
    setting_file = None
    zshrc = os.path.join(HOME, ".zshrc")
    bashrc = os.path.join(HOME, ".bashrc")
    if args.bashrc:
        setting_file = bashrc
    elif args.zshrc:
        setting_file = zshrc
    else:
        sys.stderr.write("you need enter any setting file type.\n")
        sys.exit(2)
    if args.add:
        envtmp_li = get_env_variable(env_nm)
        print("=============existing env============")
        print(envtmp_li)
        new_path = args.add
        if not os.path.exists(new_path):
            sys.stderr.write("path to add is not existing.")
            sys.exit(2)
        envtmp_li.append(new_path)
        env_va = set_env_path(envtmp_li)
        write_env_file(env_nm, env_va, setting_file)
        print("new environment has been set.")
    elif args.delete:
        envtmp_li = get_env_variable(env_nm)
        print("=============existing env============")
        print(envtmp_li)
        new_path = args.delete
        if not os.path.exists(new_path):
            sys.stderr.write("path to add is not existing.")
            sys.exit(2)
        envtmp_li.remove(new_path)
        env_va = set_env_path(envtmp_li)
        write_env_file(env_nm, env_va, setting_file)
        print("new environment has been set.")
    else:
        envtmp_li = get_env_variable(env_nm)
        print("=============existing env============")
        print(envtmp_li)
        new_env_li = confirm_path_exists(envtmp_li)
        print("=============new_env================")
        print(new_env_li)
        dif_env = set(envtmp_li) - set(new_env_li)
        print("============dif_env===============")
        print(dif_env)
        new_env_va = set_env_path(new_env_li)
        if dif_env:
            write_env_file(env_nm, new_env_va, setting_file)
