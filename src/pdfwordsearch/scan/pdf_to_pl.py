# convert pdf scan result to compress list
#
from pdfwordsearch.data_structures.abstract_postings_list import AbstractPostingsList
from pdfwordsearch.data_structures.compressed_postings_list import CompressedPostingsList
from typing import Dict, List
from collections import Counter
def pdf_to_pl(pdf: Dict[int, List[str]], postings_list: type[AbstractPostingsList]) -> AbstractPostingsList:
    """    
    Giving abstract pdf and convert it to a compressed posting List
    --
    Parameters:
    pdf : a representation of pdf scanned (used pdfScan.py to create such abstract dictionary)

    ---
    Output:
    CompressedPostingsList
    """
    pl = postings_list()
    for key, val in pdf.items():
        words = [] 
        ## all word in a single page add to the list
        for v in val:
            words.extend(wd.lower().strip() for wd in v.split())
        word_count = Counter(words)
        for w, count in word_count.items():
            pl.add_word(w, count, key)
    return pl




