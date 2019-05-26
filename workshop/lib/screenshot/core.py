#!/usr/bin/env python3

import numpy as np
from PIL import ImageGrab
import pyautogui



class ImageBox(object):
    def __init__(self, left=None,
                 top=None, bottom=None,
                 right=None):
        self.left = left
        self.top = top
        self.bottom = bottom
        self.right = right

    def enter_box_from_width_and_height(self, center, width, height):
        pass

    def box_show(self):
        pass

    def __call__(self):
        pass


class Screenshotter(object):
    def __init__(self, box_ob, shot_png_dir=None,
                 basefnm="schot{}.png"):
        pass

    def setup_screenshot(self):
        pass

    def screenshot(self):
        pass

    def gene_screenshot(self):
        while True:
            self.screenshot()
            yield


