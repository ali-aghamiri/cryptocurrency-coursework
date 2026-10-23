"""Bitcoin testnet legacy P2PKH address and WIF construction.

The encoding steps are implemented here rather than delegated to a wallet
library, mirroring the second computer assignment. This is educational code.
"""

from dataclasses import dataclass
import hashlib
import secrets

from ecdsa import SECP256k1, SigningKey


BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def hash256(data: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def hash160(data: bytes) -> bytes:
    return hashlib.new("ripemd160", hashlib.sha256(data).digest()).digest()


def base58check(payload: bytes) -> str:
    """Encode payload and four-byte checksum, preserving leading zero bytes."""
    checked = payload + hash256(payload)[:4]
    value = int.from_bytes(checked, "big")
    encoded = ""
    while value:
        value, remainder = divmod(value, 58)
        encoded = BASE58_ALPHABET[remainder] + encoded
    leading_zeroes = len(checked) - len(checked.lstrip(b"\x00"))
    return "1" * leading_zeroes + encoded


@dataclass(frozen=True)
class TestnetKey:
    private_key: bytes
    public_key: bytes
    wif: str
    address: str


def testnet_key(private_key: bytes | None = None, *, compressed: bool = True) -> TestnetKey:
    """Build a testnet key record; callers should not log private_key or wif."""
    if private_key is None:
        # The curve accepts scalars from 1 through order - 1.
        private_key = (secrets.randbelow(SECP256k1.order - 1) + 1).to_bytes(32, "big")
    if len(private_key) != 32 or not 1 <= int.from_bytes(private_key, "big") < SECP256k1.order:
        raise ValueError("Private key must be a valid 32-byte secp256k1 scalar")

    signing_key = SigningKey.from_string(private_key, curve=SECP256k1)
    raw_public = signing_key.verifying_key.to_string()
    x, y = raw_public[:32], raw_public[32:]
    public_key = (bytes([2 + (y[-1] & 1)]) + x) if compressed else (b"\x04" + raw_public)
    address = base58check(b"\x6f" + hash160(public_key))
    wif = base58check(b"\xef" + private_key + (b"\x01" if compressed else b""))
    return TestnetKey(private_key, public_key, wif, address)


def find_vanity(fragment: str, *, max_attempts: int = 100_000) -> tuple[TestnetKey, int]:
    """Find a testnet address whose characters 2.. match a short Base58 fragment."""
    if not fragment or any(char not in BASE58_ALPHABET for char in fragment):
        raise ValueError("Use a nonempty Base58 fragment")
    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")
    for attempt in range(1, max_attempts + 1):
        key = testnet_key()
        if key.address[1:].startswith(fragment):
            return key, attempt
    raise LookupError(f"No address found after {max_attempts} attempts")
