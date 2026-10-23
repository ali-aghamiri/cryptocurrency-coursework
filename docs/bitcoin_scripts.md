# Bitcoin Script exercises

These examples verify scripts against synthetic transactions. They are useful for inspecting stack conditions without needing testnet coins or a node.

| Locking condition | Unlocking data | Local result |
| --- | --- | --- |
| P2PKH (`OP_DUP OP_HASH160 … OP_EQUALVERIFY OP_CHECKSIG`) | Signature and matching public key | Pass |
| `OP_TRUE` | Empty script | Pass |
| `OP_FALSE` | Empty script | Fail |
| 2-of-3 `OP_CHECKMULTISIG` | Dummy item and two ordered signatures | Pass |
| Custom conditional | Current year and birth year, age at least 18 | Pass |
| Custom conditional | Correct password preimage | Pass |
| Custom conditional | Underage year pair or wrong password | Fail |

The custom script is a course exercise: the `OP_IF` branch subtracts birth year from current year and compares the result with 18; the `OP_ELSE` branch checks a SHA-256 preimage. A year supplied by the spender is **not** a trustworthy age proof in a real transaction. The example demonstrates Bitcoin Script control flow, not a real-world identity or access-control system.

`OP_CHECKMULTISIG` requires an extra leading stack item because of the historical off-by-one behavior described in the [Bitcoin Developer Guide](https://developer.bitcoin.org/devguide/transactions.html#multisig). The tests pass only valid signatures in the order of their public keys.
