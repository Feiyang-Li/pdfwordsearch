from pathlib import Path

import pytest
from pymupdf import pymupdf

from pdf_viewer.utilities.summary import summary

@pytest.fixture
def current_dir():
    return Path(__file__).parent

@pytest.fixture
def hello_world_path(current_dir):
    return current_dir.joinpath("../../resources/hello world.pdf")

@pytest.fixture
def hello_world_pdf(hello_world_path):
    return pymupdf.open(hello_world_path)


def test_summary(hello_world_pdf):
    actual = summary(hello_world_pdf, 0)

    expected = "Hello world"

    assert actual == expected

def test_summary_page_out_of_bounds(hello_world_pdf):
    pytest.raises(IndexError, summary, hello_world_pdf, 2)

def test_summary_characters_allowed_0(hello_world_pdf):
    actual = summary(hello_world_pdf, 0, 0)
    expected = "..."

    assert actual == expected

def test_summary_not_enough_characters(hello_world_pdf):
    actual = summary(hello_world_pdf, 0, 10)
    expected = "Hello w..."

    assert actual == expected