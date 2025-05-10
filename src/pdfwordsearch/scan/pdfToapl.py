# convert pdf scan result to compress list
# 
from pdfwordsearch.data_structures.compressed_postings_list import CompressedPostingsList
from typing import Dict, List
from collections import Counter
def pdfToAPL(pdf: Dict[int, List[str]]) -> CompressedPostingsList:
    """    
    Giving abstract pdf and convert it to a compressed posting List
    --
    Parameters:
    pdf : a representation of pdf scanned (used pdfScan.py to create such abstract dictionary)

    ---
    Output:
    CompressedPostingsList
    """
    cpl = CompressedPostingsList()
    for key, val in pdf.items():
        words = [] 
        ## all word in a single page add to the list
        for v in val:
            words.extend(wd.lower().strip() for wd in v.split())
        wordCount = Counter(words)
        for w, count in wordCount.items():
            cpl.add_word(w, count, key)
    return cpl 




