from pathlib import Path

import pytest

from pdfwordsearch.scan.pdf_scan import pdf_info_get

current_dir = Path(__file__).parent

hello_world_path = current_dir.joinpath("../resources/hello world.pdf")


@pytest.mark.parametrize("hello_world", [hello_world_path, ])
def test_pdf_scan(hello_world):
    with open(hello_world, "rb") as pdf:
        actual = pdf_info_get(pdf)

        assert actual == {
            0: ["Hello", "world"],
            1: [
                "Hello",
                "world",
                "my",
                "goodness",
                "this",
                "is",
                "page",
                "2",
                "and",
                "it",
                "has",
                "at",
                "least",
                "50",
                "characters",
            ],
        }
