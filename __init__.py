import secrets
from enum import Enum

from block_cipher_modes import cipher_block_chaining_encrypt, cipher_feedback_encrypt, output_feedback_encrypt, \
    counter_encrypt, counter_decrypt, output_feedback_decrypt, cipher_feedback_decrypt, cipher_block_chaining_decrypt, \
    IV_LENGTH


class AESModes(Enum):
    CBC = 1
    CFB = 2
    OFB = 3
    CTR = 4


def encrypt(plaintext: bytes, key: bytes, iv: bytes, mode: AESModes) -> bytes:
    match mode.name:
        case 'CBC':
            return cipher_block_chaining_encrypt(plaintext, key, iv)
        case 'CFB':
            return cipher_feedback_encrypt(plaintext, key, iv)
        case 'OFB':
            return output_feedback_encrypt(plaintext, key, iv)
        case 'CTR':
            return counter_encrypt(plaintext, key, iv)
        case _:
            raise ValueError("Invalid mode")


def decrypt(ciphertext: bytes, key: bytes, iv: bytes, mode: AESModes) -> bytes:
    match mode:
        case 'CBC':
            return cipher_block_chaining_decrypt(ciphertext, key, iv)
        case 'CFB':
            return cipher_feedback_decrypt(ciphertext, key, iv)
        case 'OFB':
            return output_feedback_decrypt(ciphertext, key, iv)
        case 'CTR':
            return counter_decrypt(ciphertext, key, iv)
        case _:
            raise ValueError("Invalid mode")


def generate_iv() -> bytes:
    return secrets.token_bytes(IV_LENGTH)
