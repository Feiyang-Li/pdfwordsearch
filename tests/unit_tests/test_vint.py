from io import BytesIO

import pytest

from pdfwordsearch.data_structures.vint import VIntReader, VIntWriter

nums = range(0, 200)


@pytest.mark.parametrize("num", list(nums))
def test_vint(num):
    byte_stream = bytearray()
    VIntWriter.write(byte_stream, num)
    actual = next(VIntReader.read(byte_stream))
    assert actual == num


def test_vint_invalid_write():
    byte_stream = bytearray()
    with pytest.raises(ValueError):
        VIntWriter.write(byte_stream, -1)


def test_vint_array():
    byte_stream = bytearray()
    _nums = [0, 1, 2]
    for num in _nums:
        VIntWriter.write(byte_stream, num)

    actual_nums = VIntReader.read(byte_stream)

    assert list(actual_nums) == _nums


def test_vint_array_large():
    byte_stream = bytearray()
    _nums = [2**128, 2**128 + 1, 2**128]

    for num in _nums:
        VIntWriter.write(byte_stream, num)

    actual_nums = VIntReader.read(byte_stream)

    assert list(actual_nums) == list(_nums)
