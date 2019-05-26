#!/usr/bin/env python3

# formal lib
import img2pdf
import os
# my lib
from help_os import ConfirmExt


class ConfirmExt(object):
    def __init__(self, fpath_ext=".png"):
        self.fpath_ext = fpath_ext
        
    def __call__(self, fnm):
        basenm, ext = os.path.splitext(
                                    fpath_ext)
        if ext != self.fpath_ext:
            emes = "{} has invalid extention:".format(fnm)
            raise TypeError(emes)
        return fnm


class ConverterToPdf(object):
    def __init__(self):
        self.png_list = []
        self.confirmer = ConfirmExt(".png")


    def add_png(self, *pngs):
        for png in pngs:
            png = self.confirmer(png)
            self.png_list.append(png)

    def add_png_from_dir(self):
        if 

    
    def _gene_converter(self):
        for png in self.png_list:
            info = img2pdf.convert(png)
            yield info

    def to_pdf(self, ofile):
        with open(ofile, "w") as write:
            for info in self._gene_converter():
                write.write(info)

    def add_pdf(self, ofile):
        with open(ofile, "a") as add:
            for info in self._gene_converter():
                add.write(info)
