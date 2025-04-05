from pdfwordsearch.query.term import tokens_to_terms, SimpleTerm
from pdfwordsearch.query.tokenizer import Token
import pytest

tokens_and_expected = [([Token("WORD", "hello"), Token("WORD", "world")], [SimpleTerm("hello"), SimpleTerm("world")])]

@pytest.mark.parametrize("tokens,expected", tokens_and_expected)
def test_tokens_to_terms(tokens, expected):
    actual = tokens_to_terms(tokens)
    assert actual == expected