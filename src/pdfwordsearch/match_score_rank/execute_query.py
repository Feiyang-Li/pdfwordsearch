import math
from collections import defaultdict
from typing import Dict, List, Tuple

from pdfwordsearch.data_structures.abstract_postings_list import AbstractPostingsList
from pdfwordsearch.match_score_rank.word_match import word_synonyms
from pdfwordsearch.query.term import tokens_to_terms, Term, NegativeTerm
from pdfwordsearch.query.tokenizer import tokenize


def execute_query(
    query: str,
    postings_list: AbstractPostingsList,
    term_match_modifier: float = 1.5,
    syn_match_modifier: float = 0.5,
) -> List[Tuple[int, float]]:
    """

    Parameters
    ----------
    syn_match_modifier :
    term_match_modifier :
    query :
    postings_list :

    Returns an ordered list of docids and scores.
    -------

    """
    terms = tokens_to_terms(tokenize(query))

    result: Dict[int, float] = defaultdict(lambda: 0)

    for term in terms:
        match term:
            case Term(value=value):
                for docid, word_count in postings_list.get_locations(value):
                    result[docid] += math.log(word_count + 1) * term_match_modifier

                try:
                    syns = word_synonyms(value)

                    for syn in syns:
                        for docid, word_count in postings_list.get_locations(syn):
                            result[docid] += math.log(word_count + 1) * syn_match_modifier
                except LookupError:
                    print("nltk package not installed. Ignoring synonyms")

            case NegativeTerm(value=value):
                for docid, word_count in postings_list.get_locations(value):
                    result[docid] -= math.log(word_count + 1) * term_match_modifier
            case _:
                raise RuntimeError(f"Unknown term type {type(term)} with value {term}")
    return sorted(result.items(), key=lambda value: value[1], reverse=True)
