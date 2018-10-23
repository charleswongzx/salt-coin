# BLOCKCHAIN PROJECT
Basic implementation of Blockchain

## Getting Started
1. Download git repo
2. In CLI, run main.py file, this implements all the blockchain functions
```
$ python main.py
```
You should get this result:


3.In CLI, run main_attack.py file, this implements the selfish mining attacks
```
$ python main_attack.py
```
You should get this result:

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
  - mine
  - send_transaction:
  - verifyTransaction:
  - updateLedger:
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

