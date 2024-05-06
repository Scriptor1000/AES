from cipher import cipher, inv_cipher
from helpers import xor_bytes, add_padding, remove_padding
from key_schedule import KeySchedule

BLOCK_LENGTH = 16
IV_LENGTH = 16
KEY_LENGTHS = [16, 24, 32]


def _encrypt_block(block, key):
    schedule = KeySchedule(key)
    return cipher(block, schedule.round_count, schedule)


def _decrypt_block(block, key):
    schedule = KeySchedule(key)
    return inv_cipher(block, schedule.round_count, schedule)


def cipher_block_chaining_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) in KEY_LENGTHS
    assert len(iv) == IV_LENGTH
    plaintext = add_padding(plaintext, BLOCK_LENGTH)  # 16 bytes = 128 bits block size
    ciphertext = b''
    for i in range(0, len(plaintext), BLOCK_LENGTH):
        block = xor_bytes(bytes(plaintext[i:i + BLOCK_LENGTH]), iv)
        block = _encrypt_block(block, key)
        ciphertext += block
        iv = block
    return ciphertext


def cipher_block_chaining_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) in KEY_LENGTHS
    assert len(iv) == IV_LENGTH
    assert len(ciphertext) % BLOCK_LENGTH == 0
    plaintext = b''
    for i in range(0, len(ciphertext), BLOCK_LENGTH):
        block = _decrypt_block(ciphertext[i:i + BLOCK_LENGTH], key)
        block = xor_bytes(block, iv)
        plaintext += block
        iv = ciphertext[i:i + 16]
    return remove_padding(plaintext)


def cipher_feedback_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) in KEY_LENGTHS
    assert len(iv) == IV_LENGTH
    plaintext = add_padding(plaintext, BLOCK_LENGTH)  # 16 bytes = 128 bits block size
    ciphertext = b''
    for i in range(0, len(plaintext), BLOCK_LENGTH):
        block = _encrypt_block(iv, key)
        iv = xor_bytes(bytes(plaintext[i:i + BLOCK_LENGTH]), block)
        ciphertext += iv
    return ciphertext


def cipher_feedback_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) in KEY_LENGTHS
    assert len(iv) == IV_LENGTH
    assert len(ciphertext) % BLOCK_LENGTH == 0
    plaintext = b''
    for i in range(0, len(ciphertext), BLOCK_LENGTH):
        block = _encrypt_block(iv, key)
        iv = ciphertext[i:i + BLOCK_LENGTH]
        plaintext += xor_bytes(iv, block)
    return remove_padding(plaintext)


def output_feedback_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) in KEY_LENGTHS
    assert len(iv) == IV_LENGTH
    return _output_feedback(add_padding(plaintext, BLOCK_LENGTH), key, iv)


def output_feedback_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) in KEY_LENGTHS
    assert len(iv) == IV_LENGTH
    assert len(ciphertext) % BLOCK_LENGTH == 0
    return remove_padding(_output_feedback(ciphertext, key, iv))


def counter_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) in KEY_LENGTHS
    assert len(iv) == IV_LENGTH
    return _counter(add_padding(plaintext, 16), key, iv)


def counter_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) in KEY_LENGTHS
    assert len(iv) == IV_LENGTH
    assert len(ciphertext) % BLOCK_LENGTH == 0
    return remove_padding(_counter(ciphertext, key, iv))


def _output_feedback(message: bytes, key: bytes, iv: bytes) -> bytes:
    result = b''
    for i in range(0, len(message), BLOCK_LENGTH):
        block = _encrypt_block(iv, key)
        result += xor_bytes(bytes(message[i:i + BLOCK_LENGTH]), block)
        iv = block
    return result


def _counter(message: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(iv) == IV_LENGTH
    assert len(message) / BLOCK_LENGTH < 2 ** 32
    result = b''
    for i in range(0, len(message), BLOCK_LENGTH):
        block = _encrypt_block(iv, key)
        result += xor_bytes(bytes(message[i:i + BLOCK_LENGTH]), block)
        iv = _increment(iv)
    return result


def _increment(iv: bytes):
    assert len(iv) == IV_LENGTH
    counter = int.from_bytes(iv[12:], 'big')
    counter += 1
    return iv[:12] + counter.to_bytes(4, 'big')
