# BLOCKCHAIN PROJECT
Basic implementation of Blockchain

## Getting Started
1. Download git repo
2. In CLI, run main.py file, this implements all the blockchain functions
```
$ python main.py
```
You should get this result:

![Mining and Verification](imgs/main_output.png)
![Blocks](imgs/main_blocks.png)
![Blocks](imgs/Balance_Checks.png)


3.In CLI, run main_attack.py file, this implements the selfish mining attacks
```
$ python main_attack.py
```
You should get this result:

![Mining and Verification](imgs/attack_output.png)
![Blocks](imgs/attack_balance.png)

## Class Functions:
Transaction class:
  - validate: Returns True/ False to whether the transaction is valid (signed by sender)
  - sign: Signs the json message
  - to_json: Converts to a json message

Block class:
  - mineBlock:
  - calculateHash:
  - proof_tree:
  - build_tree:

Blockchain class:
  - createGenesisBlock:
  - getLatestBlock:
  - add:
  - resolve:
  - checkvalidblock:

Miner class:
  - mine: Function to mine which mines the block and and updates the ledger and pushes changed to the chain
  - selfish_mine: Function to selfish mine which mines the block while not broadcasting the changes to the chain and only broadcasting the changes after mining a block first
  - update: Update function is suppose to simulate a broadcast function in a network.
  - send_transaction: Miners should have the ability to send money to other miners or clients
  - verifyTransaction:
  - updateLedger: Verify Pending Transactions and add into list of verifiedTransactions
  - getChainLedger:
  - chainvalidation:
  - getpath:


SPV class:
  - get_block_header: Return all block headers from chain
  - receive_transaction: Proof Transacation exist in block
  - send_transaction: Sends a signed transaction


## Differences between Bitcoin and your SUTDcoin:
In Bitcoin, everything is decentralised.

But for our implementation of SUTDcoin, due to constraints of network, we were not able to make it decentralised.

e.g. Our pool of transactions is a centralised pool.

## Authors
Charles Wong

Law Jia Li

Aravind Kandiah
