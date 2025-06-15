from nltk.corpus import wordnet as wn
import nltk
import difflib

def word_synonyms(word: str = "default", CI = 0.3):
    """ 
    wordSynonyms convert the word into list of words that is the 
    synonyms of the word and also additional chance of that word is added
    Input:
    word: str  
    CI: float => cutoff interval for similarity
    Output:
    list(...(word : str, clossness: int) ... )
    """
    bn = wn.synsets(word)
    if not bn:
        return []
    base_synset = bn[0]  # Choose the primary sense (adjust as needed)
    similar_words = []

    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            other_synsets = wn.synsets(lemma.name())
            if not other_synsets:
                continue

            # Just compare first sense for each synonym
            sim = base_synset.wup_similarity(other_synsets[0])
            if sim is not None and lemma.name() != word:
                if sim > CI:
                    similar_words.append((lemma.name()))

    return similar_words

    
def sim_match(wordMatch, wordOrig, CI = 0.5, test=False):
    """ 
    determine if wordMatch is similar as wordOrig
    Input:
    wordMatch: str => word to match_score_rank
    wordOrig: str => original word
    CI: float => cutoff interval for similarity
    Output:
    true/false
    """
    if test:
        print(difflib.SequenceMatcher(None, wordMatch, wordOrig).ratio())
    return difflib.SequenceMatcher(None, wordMatch, wordOrig).ratio() > CI

def match(wordMatch, wordOrig, CI_syn=0.3, CI_sim=0.5):
    # wordMatch: word we want to check if it is valid
    # wordOrig: the word we have on our hand. 
    wordSyn = word_synonyms(wordOrig, CI_syn)
    return (wordMatch in wordSyn) or (sim_match(wordMatch, wordOrig, CI_sim)) or wordMatch == wordOrig


## match_score_rank would obtain some level of change
