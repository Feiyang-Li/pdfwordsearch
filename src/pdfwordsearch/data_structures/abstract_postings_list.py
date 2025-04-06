from abc import ABC, abstractclassmethod, abstractmethod
from typing import Iterator, Tuple

from pdfwordsearch.data_structures.postings_list import PostingsList

class AbstractPostingsList(ABC):
    @abstractmethod
    def add_word(self, word: str, word_count: int, docid: int) -> None:
        """

        Parameters
        ----------
        word : a word found in the document
        word_count : number of words encountered in the document or page
        docid : the id of the document

        Returns
        -------

        """
        raise NotImplementedError()

    @abstractmethod
    def get_locations(self, word: str) -> Iterator[Tuple[int, int]]:
        """

        Parameters
        ----------
        word : a word found in the document

        Returns
        -------

        """
        raise NotImplementedError()