from io import BytesIO
from typing import Iterator, Dict

from pdfwordsearch.data_structures.postings_list import PostingsList


class CompressedPostingsList(PostingsList):
    def __init__(self):
        super().__init__()
        self.postings_list: Dict[str, BytesIO] = dict()

    def add_word(self, word: str, word_count: int, docid: int):
        if word not in self.postings_list:
            self.postings_list[word] = BytesIO()
        else:
            self.postings_list[word] += (word_count, docid)

    def get_locations(self, word: str) -> Iterator[int]:
        """

        Parameters
        ----------
        word :

        Returns
        -------

        """
        pass