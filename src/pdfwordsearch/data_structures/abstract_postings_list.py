from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Iterator, Tuple, List, Dict, Optional

from pdfwordsearch.match_score_rank.word_match import word_synonyms
from pdfwordsearch.query.term import tokens_to_terms, Term, NegativeTerm
from pdfwordsearch.query.tokenizer import tokenize
import math
from collections import Counter

class AbstractPostingsList(ABC):
    def __init__(self, pdf: Optional[Dict[int, List[str]]] = None):
        if pdf is None:
            return

        for key, val in pdf.items():
            words = []
            for v in val:
                words.extend(wd.lower().strip() for wd in v.split())
            word_count = Counter(words)
            for w, count in word_count.items():
                self._add_word(w, count, key)

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
    def get_locations(self, word: str) -> Iterator[Tuple[int, int]]:
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
                    for docid, word_count in self.get_locations(value):
                        result[docid] += math.log(word_count + 1) * term_match_modifier

                    try:
                        syns = word_synonyms(value)

                        for syn in syns:
                            for docid, word_count in self.get_locations(syn):
                                result[docid] += math.log(word_count + 1) * syn_match_modifier
                    except LookupError:
                        print("nltk package not installed. Ignoring synonyms")

                case NegativeTerm(value=value):
                    for docid, word_count in self.get_locations(value):
                        result[docid] -= math.log(word_count + 1) * term_match_modifier
                case _:
                    raise RuntimeError(f"Unknown term type {type(term)} with value {term}")
        return sorted(result.items(), key=lambda value: value[1], reverse=True)
