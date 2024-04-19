from polynom import Polynom


def get_columns(state: bytes) -> list[list[bytes]]:
    assert len(state) == 16
    return [[bytes([state[i + j]]) for j in range(4)] for i in range(0, 16, 4)]


def mix_columns(state: bytes) -> bytes:
    assert len(state) == 16
    columns = get_columns(state)
    matrix = [b'\x02', b'\x03' b'\x01', b'\x01']
    res_columns = []
    for c in range(4):
        res_c = []
        for i in range(4):
            res_c.append(Polynom(columns[c][i]) * Polynom(matrix[(c + i) % 4]) % Polynom(b'\x01\x1b'))
        res_columns.append(res_c)
    return bytes([res_columns[j][i] for i in range(4) for j in range(4)])


print(mix_columns(b'0123465789ABCDEF'))
