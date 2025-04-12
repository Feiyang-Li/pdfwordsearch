from data_structures.posting_listv2 import PostingsListV2
from pdfScan import pdfInfoGet
import string
import json

def createPostingListFrompdf(filePosition: str, encode : str = "utf8" , save : str | None = None, scanParam = {}):
    """ 
    CreatePostingListFromPdf: creating a posting list from the pdf
    filePostion: str => location of the file
    encoode: str => encoding method of the pdf
    save: str | None => save to the given location, not save if pass in as None
    scanParam: dic => parameter option for the pdfInfo Get. 
    
    """
    df = pdfInfoGet(filePosition, **scanParam)
    pl = PostingsListV2()
    for key, val in df.items():
        for sentence in val:
            translator = str.maketrans('', '', string.punctuation)
            words = sentence.translate(translator).split()
            for word in words:
                pl.add_word(word, key)
    if save:
        with open(save, "w", encoding=encode) as f:
            json.dump(pl.postings_list, f, indent=4)
    return pl