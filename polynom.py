class Polynom:
    def __init__(self, value: bytes = b''):
        binary_string = ''.join([bin(i)[2:].zfill(8) for i in value])
        self.values = list(map(int, binary_string.lstrip('0')))
        self.values.reverse()
        # LITTLE ENDIAN = Most Significant Bit last

    def most_significant_one(self):
        # Returns the Index of the most significant 1
        # That is the 1 with the highest index
        return len(self) - self.values[::-1].index(1)

    def remove_leading_zeros(self):
        while not self.values[-1]:
            self.values.pop()

    def __str__(self):
        return ' + '.join(['1' if index == 0 else f'x^{index}'
                           for index, value in enumerate(self.values) if value])

    def __getitem__(self, item):
        return 0 if item >= len(self) else self.values[item]

    def __setitem__(self, key, value):
        if key < len(self.values):
            self.values[key] = value
        else:
            self.values += [0] * (key - len(self) + 1)
            self.values[key] = value

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(self.values)

    def __bytes__(self):
        self.remove_leading_zeros()
        return bytes([int(''.join(map(str, self.values[i:i + 8][::-1])), 2)
                      for i in range(0, len(self), 8)][::-1])
