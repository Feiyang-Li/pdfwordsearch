from pathlib import Path

import pytest
from pymupdf import pymupdf

from pdfwordsearch.scan.pdf_scan import pdf_info_get



current_dir = Path(__file__).parent

hello_world_path = current_dir.joinpath("resources/hello world.pdf")

@pytest.fixture
def hello_world_pdf():
    return pymupdf.open(hello_world_path)

@pytest.fixture
def hello_world_pdf_info(hello_world_pdf):
    return pdf_info_get(file=hello_world_pdf)