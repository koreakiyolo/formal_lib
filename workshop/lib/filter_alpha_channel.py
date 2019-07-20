#!/usr/bin/env python3

from PIL import Image
from more_itertools import consume


class DelterAlphaCannel(object):
    def __init__(self, img_files):
        self.img_files = img_files

    def _gene_imgins_without_alpha(self, img_files):
        for img_fpath in img_files:
            img_pipe = Image.open(img_fpath)
            RGB_img_ins = img_pipe.convert("RGB")
            img_pipe.close()
            yield img_fpath, RGB_img_ins

    def _gene_overwrite_png(self, img_files):
        for img_fpath, RGB_img_ins in self._gene_imgins_without_alpha(
                                                                img_files)
            RGB_img_ins.save(img_fpath)
            yield

    def overwrite_pngs(self):
        raise NotImplementedError("")

    def set_write_pngs(self, new_pngs):
        self.new_pngs = new_pngs
        if len(self.new_pngs) != len(self.img_files):
            raise TypeError("new_pngs's length must be the same.")

    def output_new_pngs(self):
        raise NotImplementedError("")
