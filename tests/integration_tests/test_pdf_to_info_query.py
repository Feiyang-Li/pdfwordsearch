import pytest

from pdfwordsearch.data_structures.compressed_postings_list import CompressedPostingsList
from pdfwordsearch.data_structures.postings_list import PostingsList
from tests.test_files import hello_world_pdf

@pytest.mark.parametrize("pl_class", [CompressedPostingsList, PostingsList])
def test_pdf_to_info_query(pl_class, hello_world_pdf):
    pl = pl_class(hello_world_pdf)
    actual = pl.execute_query("Hello")
    assert actual == [(0,0)]