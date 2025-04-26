from io import BytesIO

import pytest

from pdfwordsearch.data_structures.vint import VIntReader, VIntWriter

nums = range(-122, 127)

"""@pytest.mark.parametrize("num", list(nums))
def test_vint(num):
    bytes_stream = BytesIO()
    VIntWriter.write(bytes_stream, num)
    actual = VIntReader.read(bytes_stream)
    assert actual == num"""