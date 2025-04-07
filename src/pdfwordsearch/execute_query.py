import math
from collections import defaultdict
from typing import Dict

from pdfwordsearch.data_structures.abstract_postings_list import AbstractPostingsList
from pdfwordsearch.query.term import tokens_to_terms, Term, NegativeTerm
from pdfwordsearch.query.tokenizer import tokenize


def execute_query(query: str, postings_list: AbstractPostingsList) :
    """

    Parameters
    ----------
    query :
    postings_list :

    Returns
    -------

    """
    terms = tokens_to_terms(tokenize(query))

    result: Dict[int, float] = defaultdict(lambda: 0)


    for term in terms:
        match term:
            case Term(value=value):
                pages = postings_list.get_locations(value)
                for word_count, page in pages:
                    result[page] += math.log2(word_count + 1)
            case NegativeTerm(value=value):
                pages = postings_list.get_locations(value)
                for word_count, page in pages:
                    result[page] -= math.log2(word_count + 1)
            case _:
                raise RuntimeError(f'Unknown term type {type(term)} with value {term}')
    return dict(result)



