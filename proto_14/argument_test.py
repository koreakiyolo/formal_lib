#!/usr/bin/env python3

if __name__ == "__main__":
    import argparse
    msg = ""
    parser = argparse.ArgumentParser(description=msg, fromfile_prefix_chars="@")
    parser.add_argument("--temperature", type=str, nargs="?")
    parser.add_argument("hoge", type=str, nargs="*")
    args = parser.parse_args()
    print(args)
