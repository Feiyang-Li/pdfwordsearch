from pdfwordsearch.scan.pdf_scan import pdf_to_words
from tests.test_files import hello_world_pdf

def test_pdf_to_words(hello_world_pdf):
    actual = pdf_to_words(hello_world_pdf)

    expected = [{"hello" : 1, "world" : 1}, {'2': 1,
  '50': 1,
  'and': 1,
  'at': 1,
  'characters': 1,
  'goodness': 1,
  'has': 1,
  'hello': 1,
  'is': 1,
  'it': 1,
  'least': 1,
  'my': 1,
  'page': 1,
  'this': 1,
  'world!': 1}]

    assert list(actual) == expected