from typing import Iterator, Dict, Tuple, Optional

from pdfwordsearch.data_structures.abstract_postings_list import AbstractPostingsList
from pdfwordsearch.data_structures.vint import VIntWriter, VIntReader


class CompressedPostingsList(AbstractPostingsList):
    def __init__(self, info: Optional[dict] = None):
        self.postings_list: Dict[str, bytearray] = dict()
        self.docid_prev: Dict[str, int] = dict()
        super().__init__(info)

    def get_words(self) -> Iterator[str]:
        """

        Returns an iterator over the words in the compressed postings list.
        -------

        """
        return iter(self.postings_list.keys())

    def _add_word(self, word: str, word_count: int, docid: int):
        """
        Add word, word count and docid to postings list.
        Note: The word and docid should be unique. Meaning all occurences of the word should be counted before being
        added to the postings list.

        Parameters
        ----------
        word : word to add to the postings list
        word_count : occurences of the word
        docid : document id where word is found

        Returns None
        -------

        """
        if word not in self.postings_list:
            self.postings_list[word] = bytearray()
            self.docid_prev[word] = 0

        VIntWriter.write(self.postings_list[word], word_count)
        VIntWriter.write(self.postings_list[word], docid - self.docid_prev[word])
        self.docid_prev[word] = docid

    def get_locations(self, word: str) -> Iterator[Tuple[int, int]]:
        """

        Parameters
        ----------
        word : word to get the locations for

        Returns an iterator over the word_count and docids of the word
        -------

        """
        docid_prev = 0
        if word not in self.postings_list:
            yield from ()
            return

        results = VIntReader.read(self.postings_list[word])
        while (word_count := next(results, None)) is not None:
            delta_docid = next(results)

            docid = delta_docid + docid_prev
            docid_prev = docid
            yield word_count, docid

