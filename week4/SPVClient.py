from transaction import Transaction
import ecdsa
import hashlib
import json
"""
Design and implement an `SPVClient` class.  SPV clients should implement a
simple SPV logic, i.e., they should:
- have their key pairs associated
- be able to receive block headers (not full blocks)
- be able to receive transactions (with their presence proofs) and verify them
- be able to send transactions

Integrate your implementation with your simulator from the previous exercise.
Test your implementation.
"""
class Client:
    def __init__(self):
    #generate key pair
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST192p)
        self.public_key = self.private_key.get_verifying_key()

    def get_block_header(self, miner):
    #get list of block headers from miner's chain
        headers=[]
        for block in miner.chain.chain:
            headers.append(block.header)
        return headers

    def receive_transaction(self, transaction, miner):
        headers = self.get_block_header(miner)
        # Get Path
        hash_transaction = hashlib.sha256(transaction.json_msg.encode('utf-8')).hexdigest()
        path = miner.getpath(hash_transaction)
        # compute root with path and header
        for j in path:
            if j[0] == 0:
                combined_str = str(j[1]) + str(hash_transaction)
                hash_transaction = hashlib.sha512(combined_str.encode('utf-8')).hexdigest()
            else:
                combined_str = str(hash_transaction) + str(j[1])
                hash_transaction = hashlib.sha512(combined_str.encode('utf-8')).hexdigest()
        # proof root in list of headers
        for i in headers:
            data = json.loads(i)
            if str(data.get('merkle_root')) == str(hash_transaction):
                return True
        return False

    def send_transaction(self, address, amount):
        transaction = Transaction(self.public_key.to_string(), address, amount)
        transaction.sign(transaction.json_msg, self.private_key.to_string())
        return transaction
