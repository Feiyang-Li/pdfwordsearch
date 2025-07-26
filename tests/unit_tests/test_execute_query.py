from typing import List

import pytest

from pdfwordsearch.data_structures.compressed_postings_list import CompressedPostingsList
from pdfwordsearch.data_structures.postings_list import PostingsList

query_and_matches = [("sheep", [(3, 1.0397207708399179)]), ("sheep cow", [(3, 2.6876392038420827), (4, 1.0397207708399179)])]

@pytest.fixture(params=[PostingsList, CompressedPostingsList])
def postings_list(request):
    return request.param()

@pytest.mark.parametrize("query,expected_matches", query_and_matches)
def test_execute_query(query: str, expected_matches, postings_list) -> None:
    postings_list._add_word("sheep", 1, 3)
    postings_list._add_word("cow", 2, 3)
    postings_list._add_word("cow", 1, 4)
    postings_list._add_word("cat", 1, 1)

    actual_matches = list(postings_list.execute_query(query))

    assert  sorted(actual_matches) == expected_matches


def test_word_at_page_zero(postings_list):
    postings_list._add_word("hello", 12, 0)

    actual_matches = list(postings_list.execute_query("hello"))
    assert actual_matches == [(0, 3.8474240361923053)]

