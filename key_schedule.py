from helpers import sBox, _xor_bytes, Rcon


class KeySchedule:
    def __init__(self, key: bytes):
        assert len(key) in [16, 24, 32]
        self.key = key
        self.expanded = [_Word(key[i:i + 4]) for i in range(0, len(key), 4)]
        combinations = {16: (4, 10), 24: (6, 12), 32: (8, 14)}
        self.key_words, self.round_count = combinations[len(key)]

    def __getitem__(self, item):
        # return 4 byte words
        if len(self.expanded) > item:
            return self.expanded[item]
        temp = self[item - 1]
        if item % self.key_words == 0:
            temp = _sub_word(_rot_word(temp))
            temp = temp ^ _Word(Rcon[item // self.key_words - 1])
        elif self.key_words > 6 and item % self.key_words == 4:
            temp = _sub_word(temp)
        self.expanded.append(self[item - self.key_words] ^ temp)
        return self.expanded[item].value

    def __str__(self):
        return ' - '.join([str(word) for word in self.expanded])


class _Word:
    def __init__(self, value: bytes):
        assert len(value) == 4
        self.value = value

    def __xor__(self, other):
        assert isinstance(other, _Word)
        return _Word(_xor_bytes(self.value, other.value))

    def __str__(self):
        return ' '.join([hex(i)[2:] for i in self.value])


def _rot_word(word: _Word) -> _Word:
    return _Word(word.value[1:] + word.value[:1])


def _sub_word(word: _Word) -> _Word:
    return _Word(bytes([sBox[a] for a in word.value]))


if __name__ == '__main__':
    print(KeySchedule(b'0123456789ABCDEFFEDCBA9876543210')[10])
