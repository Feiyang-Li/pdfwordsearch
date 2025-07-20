import pytest

from pdfwordsearch.data_structures.abstract_postings_list import QueryResult
from pdfwordsearch.data_structures.compressed_postings_list import (
    CompressedPostingsList,
)
from pdfwordsearch.data_structures.postings_list import PostingsList


@pytest.fixture(params=[PostingsList, CompressedPostingsList])
def postings_list(request):
    return request.param()

def test_get_locations_from_empty_pl_is_empty(postings_list):
    assert list(postings_list.get_locations("non-existent-word")) == []

def test_add_word_compressed_postings_list(postings_list):
    postings_list._add_word("hello", 12, 120)
    postings_list._add_word("hello", 11, 123)

    actual = postings_list.get_locations("hello")

    assert list(actual) == [QueryResult(word_count=12, doc_id=120), QueryResult(word_count=11, doc_id=123)]


def test_add_multiple_word_compressed_postings_list(postings_list):
    postings_list._add_word("hello", 12, 120)
    postings_list._add_word("world", 11, 123)
    postings_list._add_word("animal", 11, 124)
    postings_list._add_word("giraffe", 11, 123)

    assert list(postings_list.get_locations("hello")) == [QueryResult(12, 120)]
    assert list(postings_list.get_locations("world")) == [QueryResult(11, 123)]
    assert list(postings_list.get_locations("animal")) == [QueryResult(11, 124)]
    assert list(postings_list.get_locations("giraffe")) == [QueryResult(11, 123)]


def test_get_words_compressed_postings_list(postings_list):
    postings_list._add_word("hello", 12, 120)
    postings_list._add_word("world", 11, 123)
    postings_list._add_word("animal", 11, 124)
    postings_list._add_word("giraffe", 11, 123)

    assert list(postings_list.get_words()) == ["hello", "world", "animal", "giraffe"]

def test_add_word_postings_list(postings_list):
    postings_list._add_word("happy", 1, 0)

    actual_result = list(postings_list.get_locations("happy"))
    expected_result = [QueryResult(1,0)]

    assert actual_result == expected_result
