#!/usr/bin/env python3

# formal lib
import sys
import getpass
import os
# my lib
from admin_passwd import AESCipher
SUBOPRIONS = ["encrypt", "decrypt"]


def wio(fnm):
    wio = open(fnm, "wb")
    return wio


def fnmstr(path_str):
    if not os.path.exists(path_str):
        mes = "{} is not file.".format(
                                    path_str
                                      )
        raise OSError(mes)
    return path_str


def encrypt(input_fnm, out_pipe):
    passwd = getpass.getpass("password:")
    with open(input_fnm, "r") as read:
        string_data = read.read()
    aes_cipher_ins = AESCipher(passwd)
    out_data = aes_cipher_ins.encrypt(string_data)
    out_pipe.write(out_data)
    out_pipe.flush()
    out_pipe.close()


def decrypt(input_fnm, out_pipe):
    passwd = getpass.getpass("password:")
    with open(input_fnm, "r") as read:
        string_data = read.read()
    aes_cipher_ins = AESCipher(passwd)
    out_data = aes_cipher_ins.decrypt(string_data)
    out_pipe.write(out_data)
    out_pipe.flush()
    out_pipe.close()


if __name__ == "__main__":
    import argparse
    msg = "this program encode or decode file or strings"
    parser = argparse.ArgumentParser(
                                description=msg,
                                fromfile_prefix_chars="@")
    parser.add_argument("--encrypt_decrypt", type=str, nargs="?",
                        default="encrypt", choices=SUBOPRIONS)
    parser.add_argument("input_fnm", type=fnmstr, nargs="?")
    ex_ostyle_args = parser.add_mutually_exclusive_group(required=True)
    ex_ostyle_args.add_argument("--out_pipe", type=wio, nargs="?",
                                default=sys.stdout)
    args = parser.parse_args()
    ENCRYPT_DECRYPT = args.encrypt_decrypt
    INPUT_FNM = args.input_fnm
    OUT_PIPE = args.out_pipe
    if ENCRYPT_DECRYPT == "encrypt":
        encrypt(INPUT_FNM, OUT_PIPE)
    elif ENCRYPT_DECRYPT == "decrypt":
        decrypt(INPUT_FNM, OUT_PIPE)
    else:
        raise AssertionError("unexpected arguments are set up.")
