class State:
    def __init__(self, value: bytes):
        assert len(value) == 16
        self.value = value

    def get_columns(self) -> list[bytes]:
        return [self.value[i:i + 4] for i in range(0, 16, 4)]

    def get_rows(self) -> list[bytes]:
        return [bytes([self.value[i + j] for j in range(0, 16, 4)]) for i in range(4)]

    def map_bytes(self, func: callable) -> bytes:
        return bytes([func(byte) for byte in self.value])

    def map_columns(self, func: callable) -> list[bytes]:
        return [func(column) for column in self.get_columns()]

    def map_rows(self, func: callable) -> list[bytes]:
        new_rows = [func(row) for row in self.get_rows()]
        return [bytes([new_rows[j][i] for j in range(4)]) for i in range(4)]

    def set_rows(self, rows: list[bytes]) -> None:
        self.value = bytes().join([bytes([rows[j][i] for j in range(4)]) for i in range(4)])

    def set_columns(self, columns: list[bytes]) -> None:
        self.value = bytes().join(columns)

    def __str__(self):
        return '\n'.join([f'{' '.join([hex(i)[2:] for i in row])}' for row in self.get_rows()])


if __name__ == '__main__':
    s = State(b'0123465789ABCDEF')
    print(s)
    print(s.map_rows(lambda row: row))
