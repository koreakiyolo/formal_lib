#!/usr/bin/env python3


from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO
from io import StringIO
from bs4 import BeautifulSoup


def get_txtlines_from_docs(word_file):
    txtlines = []
    with open(word_file, "rb") as read:
        strings = read.read()
    wf_contents = BytesIO(strigs)
    cprssed_docs = ZipFile(wf_contents)
    xml_contents = cprssed_docs.read(
                        "word/document.xml")
    xml = xml_contents.decode("utf-8")
    wd_soup = BeautifulSoup(xml)
    wd_soup.f
    



def get_txtlines_from_urldocs(word_url):
    txtlines = []


def extract_txt_from_docs(word_file, wfpath):
    pass


def extract_txt_from_URLdocs(word_url, wfapth):
    pass
