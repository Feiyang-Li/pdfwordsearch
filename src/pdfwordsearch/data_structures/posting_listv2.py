## improve version of postingsList, instead of using list of tuples of (int, int)
#   here we use dict[int, int] instead, it would help for the pdf coversion. we don't need to search for the
#   number of word occurance anymore. 


from typing import Dict, List, Tuple

from abstract_postings_list import AbstractPostingsList


class PostingsListV2(AbstractPostingsList):
    def __init__(self):
        self.postings_list: Dict[str, Dict[int, int]] = dict()
        # Dict[word, Dict[docidId, wordCount]]


    def add_word(self, word: str, docid: int):
        # automatically add_word to the posting list
        if word in self.postings_list:
            if docid in self.postings_list[word]:
                self.postings_list[word][docid] = self.postings_list[word][docid] + 1
            else:
                self.postings_list[word][docid] = 1
        else: 
            self.postings_list[word] = {docid: 1}

    def get_locations(self, word: str) -> Dict[int, int]:
        return self.postings_list[word]
