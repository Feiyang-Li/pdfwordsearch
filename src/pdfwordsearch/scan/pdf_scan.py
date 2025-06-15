from typing import Dict, BinaryIO

import pymupdf
import json
import re

def pdf_to_dict(file_bytes: BinaryIO, ignore_page=None):
    """
    Given a pdf and convert it to a compressed posting List
    Parameters
    ----------
    file_bytes :
    ignore_page :

    Returns
    -------

    """
    if ignore_page is None:
        ignore_page = []

    doc = pymupdf.Document(file_bytes)
    store : Dict[int, str] = {}

    for i in range(doc.page_count):
        if i in ignore_page:
            continue
        store[i] = doc.get_page_text(i) #type: ignore[attr-defined]

    return store




def pdf_info_get(file_path, ignore_page = [], encode="utf8", save = None, is_binary = False):
    """  
    get the information from pdf (table and image not implement yet) and 
        export as dictionary. 
    filePath: string => readFile from this location
    ignore: list(...int...) => page to ignore
    encode: str => page encoding method 
    save: str | None => save read into json. 
    """
    store = {}
    if is_binary:
        doc = pymupdf.Document(stream=file_path)
    else:
        doc = pymupdf.open(file_path)
    i = 0
    for page in doc:
        if page not in ignore_page:
            txt = page.get_text("dict")
            lst = []
            for block in txt["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        aStr = " ".join([span["text"] for span in line["spans"]])
                        nStr = re.sub(r"[^\w\s]", " ", aStr) # no weird stuff
                        lst.append(nStr)
        store[i] = lst
        i = i + 1
    if save:
        with open(save, "w", encoding=encode) as f:
            json.dump(store, f, indent=4)
    return store

