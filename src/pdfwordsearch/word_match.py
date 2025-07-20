from typing import List

from nltk.corpus import wordnet as wn
import nltk
import difflib

def get_synonyms(word: str = "default", CI = 0.3) -> List[str]:
    """ 
    for a word, get its synonyms
    Input:
    word: str  
    CI: float => cutoff interval for similarity
    Output:
    list(...(word : str, clossness: int) ... )
    """
    base_synset = wn.synsets(word)[0]  # Choose the primary sense (adjust as needed)
    synonyms = []

    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            other_synsets = wn.synsets(lemma.name())
            if not other_synsets:
                continue

            # Just compare first sense for each synonym
            sim = base_synset.wup_similarity(other_synsets[0])
            if sim is not None and lemma.name() != word:
                if sim > CI:
                    synonyms.append((lemma.name()))

    return synonyms

    
def sim_match(word_match, word_orig, CI = 0.5, test=False):
    """ 
    determine if wordMatch is similar as wordOrig
    Input:
    wordMatch: str => word to match
    wordOrig: str => original word
    CI: float => cutoff interval for similarity
    Output:
    true/false
    """
    if test:
        print(difflib.SequenceMatcher(None, word_match, word_orig).ratio())
    return difflib.SequenceMatcher(None, word_match, word_orig).ratio() > CI

def match(word_match, word_orig, CI_syn, CI_sim):
    # wordMatch: word we want to check if it is valid
    # wordOrig: the word we have on our hand. 
    wordSyn = get_synonyms(word_orig, CI_syn)
    return (word_match in wordSyn) or (sim_match(word_match, word_orig, CI_sim)) or word_match == word_orig


## match would obtain some level of change
