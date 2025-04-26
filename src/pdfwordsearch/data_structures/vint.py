from io import BytesIO

MIN_SHORT_VINT = -112
MAX_SHORT_VINT = 127


class VIntWriter:
    @staticmethod
    def write(byte_stream: BytesIO, num: int):
        if MIN_SHORT_VINT <= num <= MAX_SHORT_VINT:
            byte_stream.write(num.to_bytes(length=1, byteorder='little', signed=True))
        else:
            length = -112
            if num < 0:
                num ^= -1
                length = -120

            tmp = num
            while tmp != 0:
                tmp = tmp >> 8
                length -= 1


            byte_stream.write(num.to_bytes(length=1, byteorder='little', signed=True))

            length = -(length + 120) if (length < -120) else -(length + 112)

            byte_stream.write(num.to_bytes(4, byteorder='big', signed=False))


class VIntReader:

    @staticmethod
    def read(byte_stream: BytesIO) -> int:
        first_byte = byte_stream.read(1)
        length = int(first_byte)
        if MIN_SHORT_VINT <= length <= MAX_SHORT_VINT:
            return length
        else:
            value = 0
            for i in range(length - 1):
                value = value << 8
                value += byte_stream.read(1)
            return (value ^ -1) if VIntReader._is_vint_negative(value) else value

    @staticmethod
    def _is_vint_negative(value: int) -> bool:
        return value < -120 or (MIN_SHORT_VINT <= value < 0)

    @staticmethod
    def _decode_vint_size(byte: bytes) -> int:
        value = int(byte)
        if value >= MIN_SHORT_VINT:
            return 1
        elif value < -120:
            return -119 - value
        return -111 - value
