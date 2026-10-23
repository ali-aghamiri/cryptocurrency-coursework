from cryptocurrency_coursework.bitcoin_scripts import (
    anyone_can_spend_example,
    custom_lock,
    multisig_example,
    p2pkh_example,
    verify_custom_age,
    verify_custom_password,
)


def test_p2pkh_signature_verifies():
    assert p2pkh_example()


def test_true_and_false_scripts():
    assert anyone_can_spend_example() == (True, False)


def test_two_of_three_multisig_verifies():
    assert multisig_example()


def test_custom_script_has_two_valid_paths_and_rejects_invalid_input():
    lock = custom_lock(b"sample-password")
    assert verify_custom_age(lock, 2000, 2024)
    assert not verify_custom_age(lock, 2010, 2024)
    assert verify_custom_password(lock, b"sample-password")
    assert not verify_custom_password(lock, b"wrong-password")
