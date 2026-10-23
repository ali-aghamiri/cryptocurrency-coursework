from dataclasses import replace

import pytest

from cryptocurrency_coursework.cryptography_demo import (
    aes_decrypt,
    aes_encrypt,
    generate_rsa_keypair,
    rsa_decrypt,
    rsa_encrypt,
    sign,
    verify,
)


def test_aes_round_trip_and_tamper_detection():
    key = bytes.fromhex("10" * 16)
    packet = aes_encrypt(key, b"a private message")
    assert aes_decrypt(key, packet) == b"a private message"
    changed = replace(packet, ciphertext=bytes([packet.ciphertext[0] ^ 1]) + packet.ciphertext[1:])
    with pytest.raises(ValueError):
        aes_decrypt(key, changed)


def test_aes_nonce_changes_between_encryptions():
    key = bytes.fromhex("10" * 16)
    assert aes_encrypt(key, b"same").nonce != aes_encrypt(key, b"same").nonce
    with pytest.raises(ValueError):
        aes_encrypt(b"short", b"message")


def test_rsa_encryption_and_signature():
    private, public = generate_rsa_keypair()
    message = b"coursework"
    assert rsa_decrypt(private, rsa_encrypt(public, message)) == message
    signature = sign(private, message)
    assert verify(public, message, signature)
    assert not verify(public, b"changed", signature)


def test_small_rsa_key_rejected():
    with pytest.raises(ValueError):
        generate_rsa_keypair(1024)
