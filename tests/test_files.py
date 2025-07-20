from pathlib import Path

import pytest
from pymupdf import pymupdf

current_dir = Path(__file__).parent

hello_world_path = current_dir.joinpath("resources/hello world.pdf")

chiropterans_path = current_dir.joinpath("resources/List_of_chiropterans.pdf")

@pytest.fixture
def hello_world_pdf():
    return pymupdf.open(hello_world_path)

@pytest.fixture
def chiropterans_pdf():
    return pymupdf.open(chiropterans_path)

