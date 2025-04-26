from wordMatch import wordSynonyms, simMatch
from pdfCovert import createPostingListFrompdf

def searchPostingList(word, pl, CI_syn = 0.3, CI_sim=0.9):
    """  
    searching the posting list to find if the word exist or not
    Input:
    word: str => string of word to input
    pl: posting_list => posting list to input
    CI_syn => Confidence interval of syn match
    CI_sim => Confidence interval of similarity match
    Output:
    { ... wordMatch : Location_found ...}
    """
    syn = wordSynonyms(word, CI_syn) 
    hold = {}
    for key, val in pl.postings_list.items():
        if (key in syn) or (simMatch(key, word, CI_sim)) or key == word:
            hold[key] = val
    return hold