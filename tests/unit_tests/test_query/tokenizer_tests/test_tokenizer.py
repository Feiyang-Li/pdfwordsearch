import pytest
from pdfwordsearch.query.tokenizer import Token, tokenize

query_tests = [
    (
        "zebra elephant cow",
        [Token("WORD", "zebra"), Token("WORD", "elephant"), Token("WORD", "cow")],
    ),
    (
        "Hello. World",
        [Token("WORD", "Hello"), Token("WORD", "World")],
    ),
    (
        'Hi "Weirdos"',
        [Token("WORD", "Hi"), Token("QUOTATION_MARK", '"'), Token("WORD", "Weirdos"), Token("QUOTATION_MARK", '"')],
    ),
    ("-Email", [Token("MINUS", '-'), Token("WORD", "Email")]),
    ("123", [Token("NUMBER", 123)]),
]


@pytest.mark.parametrize("query,expected", query_tests)
def test_tokenizer(query: str, expected):
    actual = list(tokenize(query))
    assert actual == expected
