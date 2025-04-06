import struct
from io import BytesIO
import bitstring

MAGIC_BYTES = bitstring.BitArray('1000').__bytes__()
MIN_SHORT_VINT = -112
MAX_SHORT_VINT = 127


class VIntWriter:
    def __init__(self, byte_stream: BytesIO):
        self.byte_stream = byte_stream

    def write(self, num: int):
        if MIN_SHORT_VINT <= num <= MAX_SHORT_VINT:
            self.byte_stream.write(MAGIC_BYTES)
            self.byte_stream.write(bytes(num >> 7))
        else:
            6


class VIntReader:
    def __init__(self, byte_stream: BytesIO):
        self.bytes = byte_stream

    def read(self):
        pass