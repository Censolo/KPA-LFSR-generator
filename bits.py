class Bits:
    """A class to represent a mutable sequence of bits."""

    def __init__(self, value, length=None):
        if isinstance(value, int):
            if length is None:
                length = value.bit_length() or 1
            self.bits = [(value >> i) & 1 == 1 for i in reversed(range(length))]
        elif isinstance(value, (bytes, bytearray)):
            self.bits = [(byte >> i) & 1 == 1 for byte in value for i in reversed(range(8))]
        else:
            self.bits = [bool(b) for b in value]

    def __len__(self):
        return len(self.bits)

    def __str__(self):
        return ''.join('1' if b else '0' for b in self.bits)

    def __repr__(self):
        return f"Bits('{str(self)}')"

    def __getitem__(self, index):
        return self.bits[index]

    def __setitem__(self, index, value):
        self.bits[index] = bool(value)

    def __xor__(self, other):
        if not isinstance(other, Bits) or len(self) != len(other):
            raise ValueError("Operands must be Bits of equal length")
        return Bits([a ^ b for a, b in zip(self.bits, other.bits)])

    def __and__(self, other):
        if not isinstance(other, Bits) or len(self) != len(other):
            raise ValueError("Operands must be Bits of equal length")
        return Bits([a & b for a, b in zip(self.bits, other.bits)])

    def __add__(self, other):
        if not isinstance(other, Bits):
            return NotImplemented
        return Bits(self.bits + other.bits)

    def __mul__(self, scalar):
        if not isinstance(scalar, int) or scalar < 0:
            raise ValueError("Can only multiply Bits by non-negative integer")
        return Bits(self.bits * scalar)

    def to_bytes(self):    
        # Pad to multiple of 8
        padded = self.bits + [False] * ((8 - len(self.bits) % 8) % 8) # In case "len" is already a multiple of 8, this ensures zero padding is added
        return bytes([
            sum((1 << (7 - i)) if bit else 0 for i, bit in enumerate(padded[j:j + 8]))
            for j in range(0, len(padded), 8)
        ])

    def append(self, bit):
        self.bits.append(bool(bit))

    def pop(self, index=-1):
        return self.bits.pop(index)

    def parity_bit(self):
        return sum(self.bits) % 2 == 1