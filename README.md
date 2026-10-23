# Cryptocurrency Coursework

Selected, reproducible work from **Cryptocurrencies** (Dr. Shariatpanahi, 2024), completed by Seyyed Ali Aghamiri at the University of Tehran. The repository reorganizes two computer assignments into small Python modules and documents a historical three-node Ethereum lab.

| Component | What it demonstrates |
| --- | --- |
| [Cryptography](src/cryptocurrency_coursework/cryptography_demo.py) | AES-128 authenticated encryption, RSA-OAEP encryption, and SHA-256/RSA signatures |
| [Bitcoin addresses](src/cryptocurrency_coursework/bitcoin_address.py) | secp256k1 public keys, Hash160, Base58Check, testnet WIF/P2PKH addresses, and bounded vanity search |
| [Bitcoin Script](src/cryptocurrency_coursework/bitcoin_scripts.py) | Locally verified P2PKH, spendable/unspendable outputs, 2-of-3 multisig, and a two-branch age/password condition |
| [Ethereum lab notes](docs/ethereum_lab.md) | Summary of the original three-node private-network experiment and its present-day compatibility limits |
| [Written work](written-work/README.md) | Three original homework submissions and a revised reading note on the Tesseract paper |

## Run locally

Python 3.10 or newer is required. From the repository root:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\python -m pip install -e ".[dev]"
.venv\Scripts\python -m pytest -q
.venv\Scripts\python examples/demo.py
```

On macOS/Linux, replace `.venv\Scripts\python` with `.venv/bin/python`. The test suite checks correct results and failure cases; the demo prints a newly generated **testnet** address but never prints a private key. The Bitcoin Script examples use synthetic inputs and verify only the spending conditions. They do not broadcast transactions or prove that a real UTXO exists.

The first assignment originally used AES-CTR with a fixed counter. This cleaned version uses a fresh nonce with AES-GCM so that tampering is detected. RSA uses 2048-bit keys and OAEP/SHA-256 for encryption. The address encoder keeps the original assignment’s manual Base58Check construction; tests compare its output with an independent library.

The source is a post-course cleanup of work submitted in 2024. Historical raw notebooks, transaction credentials, screenshots, student identifiers, and course handouts are deliberately excluded. The written homework PDFs are copies of my own submissions with student identifiers removed. All runnable examples use new or synthetic keys. The Ethereum experiment is documented separately because the Geth proof-of-work workflow used in the 2024 assignment is no longer supported in current Geth releases.

## References

- [Bitcoin Developer Guide: transactions and scripts](https://developer.bitcoin.org/devguide/transactions.html)
- [PyCryptodome documentation](https://www.pycryptodome.org/src/introduction)
- [Current Geth guidance for private networks](https://geth.ethereum.org/docs/fundamentals/kurtosis)
