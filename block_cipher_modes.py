def encrypt_block(block, key):
    return block


def decrypt_block(block, key):
    return block


def xor_bytes(a: bytes, b: bytes) -> bytes:
    assert len(a) == len(b)
    return bytes(x ^ y for x, y in zip(a, b))


def add_padding(plaintext: bytes, block_size: int) -> bytes:
    padding_size = block_size - len(plaintext) % block_size
    return plaintext + bytes([255] + [0] * (padding_size - 1))


def cipher_block_chaining_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) == 32
    assert len(iv) == 16
    plaintext = add_padding(plaintext, 16)  # 16 bytes = 128 bits block size
    ciphertext = b''
    for i in range(0, len(plaintext), 16):
        block = xor_bytes(bytes(plaintext[i:i + 16]), iv)
        block = encrypt_block(block, key)
        ciphertext += block
        iv = block
    return ciphertext


def cipher_block_chaining_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) == 32
    assert len(iv) == 16
    assert len(ciphertext) % 16 == 0
    plaintext = b''
    for i in range(0, len(ciphertext), 16):
        block = decrypt_block(ciphertext[i:i + 16], key)
        block = xor_bytes(block, iv)
        plaintext += block
        iv = ciphertext[i]
    return plaintext


def cipher_feedback_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) == 32
    assert len(iv) == 16
    plaintext = add_padding(plaintext, 16)  # 16 bytes = 128 bits block size
    ciphertext = b''
    for i in range(0, len(plaintext), 16):
        block = encrypt_block(iv, key)
        iv = xor_bytes(bytes(plaintext[i:i + 16]), block)
        ciphertext += iv
    return ciphertext


def cipher_feedback_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) == 32
    assert len(iv) == 16
    assert len(ciphertext) % 16 == 0
    plaintext = b''
    for i in range(0, len(ciphertext), 16):
        block = encrypt_block(iv, key)
        iv = ciphertext[i:i + 16]
        plaintext += xor_bytes(iv, block)
    return plaintext


def output_feedback_encrypt(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) == 32
    assert len(iv) == 16
    return _output_feedback(add_padding(plaintext, 16), key, iv)


def output_feedback_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    assert len(key) == 32
    assert len(iv) == 16
    assert len(ciphertext) % 16 == 0
    return _output_feedback(ciphertext, key, iv)


def counter_encrypt(plaintext: bytes, key: bytes, nonce: bytes) -> bytes:
    assert len(key) == 32
    assert len(nonce) == 12  # nonce length != 128 Bits IV length
    return _counter(add_padding(plaintext, 16), key, nonce)


def counter_decrypt(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
    assert len(key) == 32
    assert len(nonce) == 12  # nonce length != 128 Bits IV length
    assert len(ciphertext) % 16 == 0
    return _counter(ciphertext, key, nonce)


def _output_feedback(message: bytes, key: bytes, iv: bytes) -> bytes:
    result = b''
    for i in range(0, len(message), 16):
        block = encrypt_block(iv, key)
        result += xor_bytes(bytes(message[i:i + 16]), block)
        iv = block
    return result


def _counter(message: bytes, key: bytes, nonce: bytes) -> bytes:
    iv = nonce + bytes(4)  # 4 bytes = 32 bits counter + 12 bytes nonce = 16 bytes
    assert len(message) / 16 < 2 ** 32
    result = b''
    for i in range(0, len(message), 16):
        block = encrypt_block(iv, key)
        result += xor_bytes(bytes(message[i:i + 16]), block)
        iv = nonce + (i // 16 + 1).to_bytes(4, 'big')
    return result
