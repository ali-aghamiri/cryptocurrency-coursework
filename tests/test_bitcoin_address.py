import pytest

from cryptocurrency_coursework.bitcoin_address import base58check, find_vanity, testnet_key as make_testnet_key


def test_base58check_preserves_zero_prefix():
    assert base58check(b"\x00" + bytes(20)).startswith("1")


def test_address_and_wif_match_btclib():
    from btclib.b58 import address_from_h160, wif_from_prv_key
    from cryptocurrency_coursework.bitcoin_address import hash160

    secret = bytes.fromhex("01" * 32)
    actual = make_testnet_key(secret)
    assert actual.wif == wif_from_prv_key(secret, network="testnet", compressed=True)
    assert actual.address == address_from_h160("p2pkh", hash160(actual.public_key), "testnet")


def test_uncompressed_address_and_invalid_key():
    from btclib.b58 import address_from_h160, wif_from_prv_key
    from cryptocurrency_coursework.bitcoin_address import hash160

    secret = bytes.fromhex("02" * 32)
    actual = make_testnet_key(secret, compressed=False)
    assert actual.wif == wif_from_prv_key(secret, network="testnet", compressed=False)
    assert actual.address == address_from_h160("p2pkh", hash160(actual.public_key), "testnet")
    with pytest.raises(ValueError):
        make_testnet_key(bytes(32))


def test_vanity_search_is_bounded():
    key, attempts = find_vanity("x", max_attempts=5000)
    assert key.address[1] == "x"
    assert 1 <= attempts <= 5000
    with pytest.raises(ValueError):
        find_vanity("0")  # zero is not part of Base58
