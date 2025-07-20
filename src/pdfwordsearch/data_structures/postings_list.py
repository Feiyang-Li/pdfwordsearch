from typing import Dict, List, Tuple, Iterator, Optional

from pymupdf import Document

from pdfwordsearch.data_structures.abstract_postings_list import AbstractPostingsList, QueryResult


class PostingsList(AbstractPostingsList):
    def __init__(self, pdf: Optional[Document] = None):
        self.postings_list: Dict[str, List[Tuple[int,int]]] = dict()
        super().__init__(pdf)

    def _add_word(self, word: str, word_count: int, docid: int):
        if word_count < 0:
            raise ValueError("word_count must be positive")

        if word in self.postings_list:
            self.postings_list[word].append((word_count,docid))
        else:
            self.postings_list[word] = [(word_count,docid)]

    def get_locations(self, word: str) -> Iterator[QueryResult]:
        if not word in self.postings_list:
            return iter([])
        return map(lambda t : QueryResult(word_count=t[0], doc_id=t[1]), self.postings_list[word])

    def get_words(self) -> Iterator[str]:
        return iter(self.postings_list.keys())

