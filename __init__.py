import secrets
from block_cipher_modes import cipher_block_chaining_encrypt, cipher_feedback_encrypt, output_feedback_encrypt, \
    counter_encrypt, counter_decrypt, output_feedback_decrypt, cipher_feedback_decrypt, cipher_block_chaining_decrypt


class AESModes:
    CBC = 1
    CFB = 2
    OFB = 3
    CTR = 4


def encrypt(plaintext: bytes, key: bytes, mode: int, iv: bytes = None) -> bytes:
    match mode:
        case AESModes.CBC:
            return cipher_block_chaining_encrypt(plaintext, key, iv)
        case AESModes.CFB:
            return cipher_feedback_encrypt(plaintext, key, iv)
        case AESModes.OFB:
            return output_feedback_encrypt(plaintext, key, iv)
        case AESModes.CTR:
            return counter_encrypt(plaintext, key, iv)
        case _:
            raise ValueError("Invalid mode")


def decrypt(ciphertext: bytes, key: bytes, mode: int, iv: bytes = None) -> bytes:
    match mode:
        case AESModes.CBC:
            return cipher_block_chaining_decrypt(ciphertext, key, iv)
        case AESModes.CFB:
            return cipher_feedback_decrypt(ciphertext, key, iv)
        case AESModes.OFB:
            return output_feedback_decrypt(ciphertext, key, iv)
        case AESModes.CTR:
            return counter_decrypt(ciphertext, key, iv)
        case _:
            raise ValueError("Invalid mode")


def generate_iv() -> bytes:
    return secrets.token_bytes(16)
