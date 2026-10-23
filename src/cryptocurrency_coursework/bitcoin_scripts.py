"""Offline Bitcoin Script exercises from the second computer assignment.

Every input refers to a synthetic UTXO. The interpreter verifies spending
conditions locally; no wallet, Bitcoin node, or network connection is used.
"""

import hashlib

from btclib.script import serialize
from btclib.script.engine import ScriptError, verify_input
from btclib.script.sig_hash import legacy
from btclib.tx import OutPoint, Tx, TxIn, TxOut
from btclib_ecc.ecc import dsa

from .bitcoin_address import hash160, testnet_key


SIGHASH_ALL = 1


def _synthetic_transaction(lock: bytes, unlock: bytes = b"") -> tuple[list[TxOut], Tx]:
    prevouts = [TxOut(2_000, lock)]
    tx = Tx(
        vin=[TxIn(OutPoint(bytes.fromhex("11" * 32), 0), unlock)],
        vout=[TxOut(1_000, serialize(["OP_TRUE"]))],
    )
    return prevouts, tx


def _signature(lock: bytes, tx: Tx, secret: bytes) -> bytes:
    digest = legacy(lock, tx, 0, SIGHASH_ALL)
    der = dsa.sign_(digest, int.from_bytes(secret, "big")).serialize()
    return der + bytes([SIGHASH_ALL])


def _verifies(lock: bytes, unlock: bytes) -> bool:
    prevouts, tx = _synthetic_transaction(lock, unlock)
    try:
        verify_input(prevouts, tx, 0)
    except ScriptError:
        return False
    return True


def p2pkh_example() -> bool:
    key = testnet_key(bytes.fromhex("01" * 32))
    lock = serialize([
        "OP_DUP", "OP_HASH160", hash160(key.public_key), "OP_EQUALVERIFY", "OP_CHECKSIG"
    ])
    _, tx = _synthetic_transaction(lock)
    unlock = serialize([_signature(lock, tx, key.private_key), key.public_key])
    return _verifies(lock, unlock)


def anyone_can_spend_example() -> tuple[bool, bool]:
    return _verifies(serialize(["OP_TRUE"]), b""), _verifies(serialize(["OP_FALSE"]), b"")


def multisig_example() -> bool:
    keys = [testnet_key(bytes([i]) * 32) for i in (2, 3, 4)]
    lock = serialize(["OP_2", *(key.public_key for key in keys), "OP_3", "OP_CHECKMULTISIG"])
    _, tx = _synthetic_transaction(lock)
    signatures = [_signature(lock, tx, key.private_key) for key in keys[:2]]
    unlock = serialize(["OP_0", *signatures])  # Required historical CHECKMULTISIG dummy item.
    return _verifies(lock, unlock)


def custom_lock(password: bytes) -> bytes:
    """Spend with age >= 18 or by revealing a SHA-256 password preimage."""
    if not password:
        raise ValueError("A nonempty password is required")
    return serialize([
        "OP_IF", "OP_SUB", 18, "OP_GREATERTHANOREQUAL",
        "OP_ELSE", "OP_SHA256", hashlib.sha256(password).digest(), "OP_EQUAL", "OP_ENDIF",
    ])


def verify_custom_age(lock: bytes, birth_year: int, current_year: int) -> bool:
    # OP_SUB consumes current_year then birth_year, yielding current - birth.
    return _verifies(lock, serialize([current_year, birth_year, "OP_TRUE"]))


def verify_custom_password(lock: bytes, password: bytes) -> bool:
    return _verifies(lock, serialize([password, "OP_FALSE"]))
