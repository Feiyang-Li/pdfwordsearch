import dataclasses
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Iterator, Tuple, List, Dict, Optional

from pdfwordsearch.match_score_rank.word_match import word_synonyms
from pdfwordsearch.query.term import tokens_to_terms, Term, NegativeTerm
from pdfwordsearch.query.tokenizer import tokenize
import math
from pymupdf import Document

from pdfwordsearch.scan.pdf_scan import pdf_to_words

@dataclasses.dataclass
class QueryResult:
    word_count: int
    doc_id: int

    def __iter__(self):
        return iter(dataclasses.astuple(self))

class AbstractPostingsList(ABC):
    def __init__(self, pdf: Optional[Document] = None):
        if pdf is None:
            return

        pages = pdf_to_words(pdf)

        for i, page in enumerate(pages):
            for word, count in page.items():
                self._add_word(word, count, i)


    @abstractmethod
    def _add_word(self, word: str, word_count: int, docid: int) -> None:
        """
        Words must be added in non-decreasing order.
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
    def get_locations(self, word: str) -> Iterator[QueryResult]:
        """

        Parameters
        ----------
        word : a word found in the document

        Returns
        -------

        """
        raise NotImplementedError()

    @abstractmethod
    def get_words(self) -> Iterator[str]:
        """

        Returns
        -------
        All words encountered in the document
        """
        raise NotImplementedError()


    def execute_query(
            self,
            query: str,
            term_match_modifier: float = 1.5,
            syn_match_modifier: float = 0.5,
    ) -> List[Tuple[int, float]]:
        """

        Parameters
        ----------
        syn_match_modifier :
        term_match_modifier :
        query :

        Returns an ordered list of docids and scores.
        -------

        """
        terms = tokens_to_terms(tokenize(query))

        result: Dict[int, float] = defaultdict(lambda: 0)

        for term in terms:
            match term:
                case Term(value=value):
                    value = value.lower()
                    for word_count, docid in self.get_locations(value):
                        result[docid] += math.log(word_count + 1) * term_match_modifier

                    try:
                        syns = word_synonyms(value)

                        for syn in syns:
                            for word_count, docid in self.get_locations(syn):
                                result[docid] += math.log(word_count + 1) * syn_match_modifier
                    except LookupError:
                        print("nltk package not installed. Ignoring synonyms")

                case NegativeTerm(value=value):
                    for word_count, docid in self.get_locations(value):
                        result[docid] -= math.log(word_count + 1) * term_match_modifier
                case _:
                    raise RuntimeError(f"Unknown term type {type(term)} with value {term}")
        return sorted(result.items(), key=lambda value: value[1], reverse=True)