#!/usr/bin/env python3

import os
import argparse
from argparse import RawTextHelpFormatter
from datetime import datetime
from help_ics import AdminICS
NOW_TIME = datetime.now()
THIS_YEAR = NOW_TIME.year


def fnmstr(path_str):
    if not os.path.exists(path_str):
        mes = "{} is not file.".format(
                                    path_str
                                      )
        raise OSError(mes)
    return path_str


if __name__ == "__main__":
    msg = "this program makes ics file."
    parser = argparse.ArgumentParser(
                            description=msg,
                            fromfile_prefix_chars="@",
                            formatter_class=RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest="sub_opt")
    csv_parser = subparsers.add_parser("csv")
    csv_parser.add_argument("--to_csv", type=str, nargs="?",
                            required=True)
    ics_parser = subparsers.add_parser("ics")
    ics_parser.add_argument("--input_csv", type=fnmstr,
                            nargs="?", required=True)
    ics_parser.add_argument("--to_ics", type=str, nargs="?", required=True)
    args = parser.parse_args()
    SUB_OPT = args.sub_opt
    if SUB_OPT == "csv":
        TO_CSV = args.to_csv
        AdminICS.to_base_csv(TO_CSV)
    elif SUB_OPT == "ics":
        INPUT_CSV = args.input_csv
        TO_ICS = args.to_ics
        admin_ics = AdminICS(INPUT_CSV)
        admin_ics.to_ics(TO_ICS)
    else:
        raise AssertionError("")
