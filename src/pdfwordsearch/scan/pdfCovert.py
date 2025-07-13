from pdf_scan import pdf_info_get
import string
import json

from pdfwordsearch.data_structures.postings_list import PostingsList



def createPostingListFrompdf(filePosition: str, encode : str = "utf8" , save : str | None = None, scanParam = {}):
    """ 
    CreatePostingListFromPdf: creating a posting list from the pdf
    filePostion: str => location of the file
    encoode: str => encoding method of the pdf
    save: str | None => save to the given location, not save if pass in as None
    scanParam: dic => parameter option for the pdfInfo Get. 
    
    """
    df = pdf_info_get(filePosition, **scanParam)
    pl = PostingsList()
    store = {}
    for key, val in df.items():
        word_count = {}
        for sentence in val:
            translator = str.maketrans('', '', string.punctuation)
            words = sentence.translate(translator).split()
            for word in words:
                w = word.lower() 
                word_count[w] = word_count.get(w, 0) + 1
        store[key] = word_count

    for key, val in store.items():
        docid = key
        secVal = val
        for word, count in secVal.items():
            pl._add_word(word, count, docid)

    if save:
        with open(save, "w", encoding=encode) as f:
            json.dump(pl.postings_list, f, indent=4)
    return pl