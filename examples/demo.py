"""Run local examples without a node, wallet, or network connection."""

from Crypto.Random import get_random_bytes

from cryptocurrency_coursework.bitcoin_address import testnet_key
from cryptocurrency_coursework.bitcoin_scripts import (
    anyone_can_spend_example,
    custom_lock,
    multisig_example,
    p2pkh_example,
    verify_custom_age,
    verify_custom_password,
)
from cryptocurrency_coursework.cryptography_demo import (
    aes_decrypt,
    aes_encrypt,
    generate_rsa_keypair,
    rsa_decrypt,
    rsa_encrypt,
    sign,
    verify,
)


def main() -> None:
    message = b"A reproducible cryptocurrency coursework demonstration."
    symmetric_key = get_random_bytes(16)
    packet = aes_encrypt(symmetric_key, message)
    assert aes_decrypt(symmetric_key, packet) == message

    private, public = generate_rsa_keypair()
    assert rsa_decrypt(private, rsa_encrypt(public, message)) == message
    assert verify(public, message, sign(private, message))

    address = testnet_key().address
    assert p2pkh_example()
    assert anyone_can_spend_example() == (True, False)
    assert multisig_example()
    lock = custom_lock(b"course-example-only")
    assert verify_custom_age(lock, 2000, 2024)
    assert verify_custom_password(lock, b"course-example-only")
    print("Cryptography, address construction, and offline Bitcoin Script checks passed.")
    print(f"Example testnet address: {address}")
    print("No private keys were printed and no transaction was broadcast.")


if __name__ == "__main__":
    main()
