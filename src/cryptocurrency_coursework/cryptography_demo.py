"""AES, RSA encryption, and digital signatures from the first computer assignment.

The submitted notebook used AES-CTR with a fixed counter. This version uses
authenticated AES-128-GCM with a fresh nonce for each message.
"""

from dataclasses import dataclass

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


@dataclass(frozen=True)
class EncryptedMessage:
    nonce: bytes
    ciphertext: bytes
    tag: bytes


def aes_encrypt(key: bytes, plaintext: bytes) -> EncryptedMessage:
    """Encrypt and authenticate bytes with AES-128-GCM."""
    if len(key) != 16:
        raise ValueError("AES-128 requires a 16-byte key")
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return EncryptedMessage(cipher.nonce, ciphertext, tag)


def aes_decrypt(key: bytes, message: EncryptedMessage) -> bytes:
    """Reject modified ciphertext or tags before returning plaintext."""
    if len(key) != 16:
        raise ValueError("AES-128 requires a 16-byte key")
    cipher = AES.new(key, AES.MODE_GCM, nonce=message.nonce)
    return cipher.decrypt_and_verify(message.ciphertext, message.tag)


def generate_rsa_keypair(bits: int = 2048) -> tuple[RSA.RsaKey, RSA.RsaKey]:
    if bits < 2048:
        raise ValueError("Use at least 2048 bits for this demonstration")
    private_key = RSA.generate(bits)
    return private_key, private_key.public_key()


def rsa_encrypt(public_key: RSA.RsaKey, plaintext: bytes) -> bytes:
    return PKCS1_OAEP.new(public_key, hashAlgo=SHA256).encrypt(plaintext)


def rsa_decrypt(private_key: RSA.RsaKey, ciphertext: bytes) -> bytes:
    return PKCS1_OAEP.new(private_key, hashAlgo=SHA256).decrypt(ciphertext)


def sign(private_key: RSA.RsaKey, message: bytes) -> bytes:
    return pkcs1_15.new(private_key).sign(SHA256.new(message))


def verify(public_key: RSA.RsaKey, message: bytes, signature: bytes) -> bool:
    try:
        pkcs1_15.new(public_key).verify(SHA256.new(message), signature)
    except (ValueError, TypeError):
        return False
    return True
