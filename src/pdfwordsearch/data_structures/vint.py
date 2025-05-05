from typing import Iterator

class VIntWriter:
    @staticmethod
    def write(integer_bytes: bytearray, value: int):
        """

        Parameters
        ----------
        integer_bytes : byte array to write the value to
        value : non-negative integer

        Returns
        -------

        """
        if value < 0:
            raise ValueError("Only non-negative integers can be encoded.")

        while value > 0x7F:
            integer_bytes.append((value & 0x7F) | 0x80)  # Set the high bit
            value >>= 7
        integer_bytes.append(value & 0x7F)  # Append the last byte


class VIntReader:
    @staticmethod
    def read(integer_bytes: bytearray) -> Iterator[int]:
        """

        Parameters
        ----------
        integer_bytes : bytes that represent a variable-length integer array

        Returns a generator of integers corresponding to the given bytes.
        -------

        """
        value = 0
        shift = 0

        for byte in integer_bytes:
            value |= (byte & 0x7F) << shift
            shift += 7
            if byte & 0x80 == 0:  # If the high bit is not set, we're done
                yield value
                value = 0
                shift = 0







