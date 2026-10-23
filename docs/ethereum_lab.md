# Three-node Ethereum lab (2024)

The second course project included a local three-node Geth network. In the original 2024 submission, I configured a genesis block and three accounts, initialized three node data directories, connected the peers, submitted a transfer, and observed it included in a mined block. The submitted report recorded peer counts, transaction status, block information, and balance changes.

This page is a summary of that historical experiment, not a command sequence for current Geth. The course used a standalone proof-of-work private-chain setup. **Current Geth cannot seal Ethash or Clique blocks on its own**; modern multi-node private networks need execution and consensus clients. For a runnable contemporary setup, use the [official Geth private-network guide with Kurtosis](https://geth.ethereum.org/docs/fundamentals/kurtosis).

The original report and configuration are kept outside this public repository because they contain student identifiers, account details, and screenshots. No keys, passwords, personalized genesis allocations, or node data are published here.
