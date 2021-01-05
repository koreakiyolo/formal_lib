#!/usr/bin/env python3


from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO
from bs4 import BeautifulSoup


def _gene_txtline_from_docs(word_file):
    with open(word_file, "rb") as read:
        strings = read.read()
    wf_contents = BytesIO(strings)
    cprssed_docs = ZipFile(wf_contents)
    xml_contents = cprssed_docs.read(
                        "word/document.xml")
    xml = xml_contents.decode("utf-8")
    wd_soup = BeautifulSoup(xml)
    txt_elms = wd_soup.find_all("w:t")
    for txt_elm in txt_elms:
        yield txt_elm.text


def _gene_txtline_from_urldocs(word_url):
    strings = urlopen(word_url).read()
    wf_contents = BytesIO(strings)
    cprssed_docs = ZipFile(wf_contents)
    xml_contents = cprssed_docs.read(
                        "word/document.xml")
    xml = xml_contents.decode("utf-8")
    wd_soup = BeautifulSoup(xml)
    txt_elms = wd_soup.find_all("w:t")
    for txt_elm in txt_elms:
        yield txt_elm.txt


def get_txtlines_from_docs(word_file):
    line_iter = _gene_txtline_from_docs(word_file)
    txt_lines = []
    for line in line_iter:
        txt_lines.append(line)
    return txt_lines


def get_txtlines_from_urldocs(word_url):
    line_iter = _gene_txtline_from_urldocs(word_url)
    txt_lines = []
    for line in line_iter:
        txt_lines.append(line)
    return txt_lines


def extract_txt_from_docs(word_file, wfpath):
    line_iter = _gene_txtline_from_docs(word_file)
    with open(wfpath, "w") as write:
        for line in line_iter:
            write.write(line + "\n")


def extract_txt_from_URLdocs(word_url, wfpath):
    line_iter = _gene_txtline_from_urldocs(word_url)
    with open(wfpath, "w") as write:
        for line in line_iter:
            write.write(line + "\n")
