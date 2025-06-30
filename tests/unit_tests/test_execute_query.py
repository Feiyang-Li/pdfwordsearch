from typing import List

import pytest

from pdfwordsearch.data_structures.postings_list import PostingsList

query_and_matches = [("sheep", {3:1}), ("sheep cow", {3:4,4:1})]

@pytest.mark.parametrize("query,expected_matches", query_and_matches)
def test_execute_query(query: str, expected_matches: List[int]) -> None:
    postings_list = PostingsList()

    postings_list._add_word("sheep", 1, 3)
    postings_list._add_word("cow", 2, 3)
    postings_list._add_word("cow", 1, 4)
    postings_list._add_word("cat", 1, 1)

    actual_matches = list(postings_list.execute_query(query))

    assert  sorted(actual_matches) == sorted(expected_matches)