from polynom import Polynom
from state import State


def _xor_bytes(a: bytes, b: bytes) -> bytes:
    assert len(a) == len(b)
    return bytes(x ^ y for x, y in zip(a, b))


def _multiply_with_polynom(byte: bytes, polynom: Polynom) -> bytes:
    return bytes(Polynom(byte) * polynom % Polynom(b'\x01\x1b'))


def _multiply_with_matrix(columns: bytes, matrix: bytes) -> bytes:
    matrix = [Polynom(bytes([b])) for b in matrix]
    new_column = []
    for _ in range(4):
        temp = [_multiply_with_polynom(bytes([columns[0]]), matrix[0]),
                _multiply_with_polynom(bytes([columns[1]]), matrix[1]),
                _multiply_with_polynom(bytes([columns[2]]), matrix[2]),
                _multiply_with_polynom(bytes([columns[3]]), matrix[3])]
        new_column.append(_xor_bytes(_xor_bytes(_xor_bytes(temp[0], temp[1]), temp[2]), temp[3]))
        matrix = [matrix[-1]] + matrix[:-1]
    return bytes().join(new_column)


def mix_columns(state: State) -> State:
    matrix = b'\x02\x03\x01\x01'
    state.set_columns(state.map_columns(lambda column: _multiply_with_matrix(column, matrix)))
    return state


def inv_mix_columns(state: State) -> State:
    matrix = b'\x0e\x0b\x0d\x09'
    state.set_columns(state.map_columns(lambda column: _multiply_with_matrix(column, matrix)))
    return state


if __name__ == '__main__':
    print(State(b'0123465789ABCDEF'))
    print(inv_mix_columns(mix_columns(State(b'0123465789ABCDEF'))))
