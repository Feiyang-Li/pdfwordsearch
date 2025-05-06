from pdfwordsearch.data_structures.compressed_postings_list import (
    CompressedPostingsList,
)


def test_add_word_compressed_postings_list():
    posting_list = CompressedPostingsList()
    posting_list.add_word("hello", 12, 120)
    posting_list.add_word("hello", 11, 123)

    actual = posting_list.get_locations("hello")

    assert list(actual) == [(12, 120), (11, 123)]


def test_add_multiple_word_compressed_postings_list():
    posting_list = CompressedPostingsList()
    posting_list.add_word("hello", 12, 120)
    posting_list.add_word("world", 11, 123)
    posting_list.add_word("animal", 11, 124)
    posting_list.add_word("giraffe", 11, 123)

    assert list(posting_list.get_locations("hello")) == [(12, 120)]
    assert list(posting_list.get_locations("world")) == [(11, 123)]
    assert list(posting_list.get_locations("animal")) == [(11, 124)]
    assert list(posting_list.get_locations("giraffe")) == [(11, 123)]


def test_get_words_compressed_postings_list():
    posting_list = CompressedPostingsList()
    posting_list.add_word("hello", 12, 120)
    posting_list.add_word("world", 11, 123)
    posting_list.add_word("animal", 11, 124)
    posting_list.add_word("giraffe", 11, 123)

    assert list(posting_list.get_words()) == ["hello", "world", "animal", "giraffe"]
