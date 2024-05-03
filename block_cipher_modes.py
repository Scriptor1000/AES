from cipher import cipher, inv_cipher
from helpers import xor_bytes, add_padding, remove_padding
from key_schedule import KeySchedule


def _encrypt_block(block, key):
    schedule = KeySchedule(key)
    return cipher(block, schedule.round_count, schedule)


def _decrypt_block(block, key):
    schedule = KeySchedule(key)
    return inv_cipher(block, schedule.round_count, schedule)


def cipher_block_chaining_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) in [16, 24, 32]
    assert len(iv) == 16
    plaintext = add_padding(plaintext, 16)  # 16 bytes = 128 bits block size
    ciphertext = b''
    for i in range(0, len(plaintext), 16):
        block = xor_bytes(bytes(plaintext[i:i + 16]), iv)
        block = _encrypt_block(block, key)
        ciphertext += block
        iv = block
    return ciphertext


def cipher_block_chaining_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) in [16, 24, 32]
    assert len(iv) == 16
    assert len(ciphertext) % 16 == 0
    plaintext = b''
    for i in range(0, len(ciphertext), 16):
        block = _decrypt_block(ciphertext[i:i + 16], key)
        block = xor_bytes(block, iv)
        plaintext += block
        iv = ciphertext[i:i + 16]
    return remove_padding(plaintext)


def cipher_feedback_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) in [16, 24, 32]
    assert len(iv) == 16
    plaintext = add_padding(plaintext, 16)  # 16 bytes = 128 bits block size
    ciphertext = b''
    for i in range(0, len(plaintext), 16):
        block = _encrypt_block(iv, key)
        iv = xor_bytes(bytes(plaintext[i:i + 16]), block)
        ciphertext += iv
    return ciphertext


def cipher_feedback_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) in [16, 24, 32]
    assert len(iv) == 16
    assert len(ciphertext) % 16 == 0
    plaintext = b''
    for i in range(0, len(ciphertext), 16):
        block = _encrypt_block(iv, key)
        iv = ciphertext[i:i + 16]
        plaintext += xor_bytes(iv, block)
    return remove_padding(plaintext)


def output_feedback_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) in [16, 24, 32]
    assert len(iv) == 16
    return _output_feedback(add_padding(plaintext, 16), key, iv)


def output_feedback_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) in [16, 24, 32]
    assert len(iv) == 16
    assert len(ciphertext) % 16 == 0
    return remove_padding(_output_feedback(ciphertext, key, iv))


def counter_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) in [16, 24, 32]
    assert len(iv) == 16
    return _counter(add_padding(plaintext, 16), key, iv)


def counter_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) in [16, 24, 32]
    assert len(iv) == 16
    assert len(ciphertext) % 16 == 0
    return remove_padding(_counter(ciphertext, key, iv))


def _output_feedback(message: bytes, key: bytes, iv: bytes) -> bytes:
    result = b''
    for i in range(0, len(message), 16):
        block = _encrypt_block(iv, key)
        result += xor_bytes(bytes(message[i:i + 16]), block)
        iv = block
    return result


def _counter(message: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(iv) == 16
    assert len(message) / 16 < 2 ** 32
    result = b''
    for i in range(0, len(message), 16):
        block = _encrypt_block(iv, key)
        result += xor_bytes(bytes(message[i:i + 16]), block)
        iv = _increment(iv)
    return result


def _increment(iv: bytes):
    assert len(iv) == 16
    counter = int.from_bytes(iv[12:], 'big')
    counter += 1
    return iv[:12] + counter.to_bytes(4, 'big')


if __name__ == '__main__':
    inp = (b'\x32\x43\xf6\xa8\x88\x5a\x30\x8d\x31\x31\x98\xa2\xe0\x39\x07\x34'
           b'\x32\x43\x26\xa8\x8a\x5a\x30\x8d\x31\x31\x98\xa3\xe0\x37\x07\x34'
           b'\x32\x43\xf6\xf8\x88\x5a\x30\x8d\x31\x31\x98\xa2\xe0\x37\x01\x34')
    key = b'\x2b\x7e\x15\x16\x28\xae\xd2\xa6\xab\xf7\x15\x88\x09\xcf\x4f\x3c'
    iv = b'\x00' * 16
    enc = cipher_block_chaining_encrypt(inp, key, iv)
    print(cipher_block_chaining_decrypt(enc, key, iv) == inp)
    enc = cipher_feedback_encrypt(inp, key, iv)
    print(cipher_feedback_decrypt(enc, key, iv) == inp)
    enc = output_feedback_encrypt(inp, key, iv)
    print(output_feedback_decrypt(enc, key, iv) == inp)
    enc = counter_encrypt(inp, key, iv)
    print(counter_decrypt(enc, key, iv) == inp)
