from pdfwordsearch.match_score_rank.word_match import word_synonyms


def test_synonyms():
    word_synonyms("hello")

    assert word_synonyms("hello") == ["hello"]