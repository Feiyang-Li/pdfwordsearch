from pdfwordsearch.data_structures.postings_list import PostingsList


def test_add_word_postings_list():
    postings_list = PostingsList()
    postings_list._add_word("happy", 0, 1)

    actual_result = postings_list.get_locations("happy")
    expected_result = [(0,1)]

    assert actual_result == expected_result
