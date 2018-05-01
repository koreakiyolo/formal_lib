#!/usr/bin/env python3
# !coding:utf-8


import pyautogui


def load_txt(txt_path):
    with open(txt_path, "r") as read:
        txt_lines = [one_line.strip() for one_line
                     in read.readlines()]
    return txt_lines


def enter_info(txt_lines, press_enter=True):
    for one_line in txt_lines:
        pyautogui.typewrite(one_line)
        pyautogui.press('tab')
    print("complete entering messages."
          "after that, it presses enter")
    pyautogui.press("enter")


if __name__ == "__main__":
    import argparse
    msg = "this program help to enter some information automatically."
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument("file_path", nargs="?",
                        type=str)
    parser.add_argument("--press_enter", default=True, action="store_false")
    args = parser.parse_args()
    FILE_PATH = args.file_path
    if FILE_PATH is None:
        raise AttributeError("program is stopped.")
    BOOL_PENTER = args.press_enter
    txt_lines = load_txt(FILE_PATH)
    enter_info(txt_lines, BOOL_PENTER)
