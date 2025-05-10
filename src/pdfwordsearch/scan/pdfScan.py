import pymupdf
import json
import re
def pdfInfoGet(filePath, ignorePage = [], encode="utf8", save = None):
    """  
    get the information from pdf (table and image not implement yet) and 
        export as dictionary. 
    filePath: string => readFile from this location
    ignore: list(...int...) => page to ignore
    encode: str => page encoding method 
    save: str | None => save read into json. 
    """
    store = {}
    doc = pymupdf.open(filePath)
    i = 0
    for page in doc:
        if page not in ignorePage:
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

