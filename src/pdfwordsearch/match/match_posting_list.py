from pdfwordsearch.match.word_match import word_synonyms, sim_match
from pdfwordsearch.data_structures.abstract_postings_list import AbstractPostingsList

def redated_searchPostingList(word, pl, CI_syn = 0.3, CI_sim=0.9):
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
    syn = word_synonyms(word, CI_syn) 
    hold = {}
    for key, val in pl.postings_list.items(): # O(n) where n is the length of pdf page. 
        if (key in syn) or (sim_match(key, word, CI_sim)) or key == word:
            hold[key] = val
    return hold

def search_posting_list(word, pl : AbstractPostingsList, CI_syn = 0.3, CI_sim=0.9):
    """ 
    Update to the redated_searchPostingList, instead of loop through the document, we loop through all words find in the
      posting_list
        word: str => string of word to input
    pl: posting_list => posting list to input
    CI_syn => Confidence interval of syn match
    CI_sim => Confidence interval of similarity match
    { ... wordMatch : Location_found ...}
    """
    #find the word:
    syn = word_synonyms(word, CI_syn) 
    hold = {}
    wds = pl.get_words()
    for wd in wds:
        if (wd in syn) or (sim_match(wd, word, CI_sim)) or wd == word:
            hold[wd] = pl.get_locations(wd)
    return hold

