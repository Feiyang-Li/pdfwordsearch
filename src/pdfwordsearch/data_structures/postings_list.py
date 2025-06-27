from typing import Dict, List, Tuple, Iterator

from pdfwordsearch.data_structures.abstract_postings_list import AbstractPostingsList


class PostingsList(AbstractPostingsList):
    def __init__(self):
        self.postings_list: Dict[str, List[Tuple[int,int]]] = dict()

    def add_word(self, word: str, word_count: int, docid: int):
        if word in self.postings_list:
            self.postings_list[word].append((word_count,docid))
        else:
            self.postings_list[word] = [(word_count,docid)]

    def get_locations(self, word: str) -> List[Tuple[int,int]]:
        if not word in self.postings_list:
            return []
        return self.postings_list[word]

    def get_words(self) -> Iterator[str]:
        return iter(self.postings_list.keys())

