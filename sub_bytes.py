from helpers import sBox, inv_sBox
from polynom import Polynom
from state import State


def _multiplicative_inverse(a: bytes) -> bytes:
    assert len(a) == 1
    if a == b'\x00': return a
    inverse = pow(Polynom(a), 254, Polynom(b'\x01\x1b'))
    return bytes(inverse)


def _affine_transformation(a: bytes) -> bytes:
    new = ''
    bits = list(map(int, ''.join([bin(i)[2:].zfill(8) for i in a])))[::-1]
    c = [0, 1, 1, 0, 0, 0, 1, 1][::-1]
    for i in range(8):
        new += str(bits[i] ^ bits[(i + 4) % 8] ^ bits[(i + 5) % 8] ^ bits[(i + 6) % 8] ^ bits[(i + 7) % 8] ^ c[i])
    return bytes([int(new[::-1], 2)])


def _test_forward():
    for i in range(256):
        b = bytes([i])
        assert bytes([sBox[i]]) == _affine_transformation(_multiplicative_inverse(b))


def sub_bytes(state: State) -> State:
    return State(state.map_bytes(lambda byte: sBox[byte]))


def inv_sub_bytes(state: State) -> State:
    return State(state.map_bytes(lambda byte: inv_sBox[byte]))
