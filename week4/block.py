import ecdsa
import hashlib
import json,random
from collections import OrderedDict
from transaction import Transaction

class Block(object):
    def __init__(self, timestamp, transactions, previousHash=''):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previousHash = previousHash
        self.nonce = 0
        self.difficulty=4
        self.hash = self.calculateHash()
        self.header = json.dumps(OrderedDict({ 'previousHash' : self.previousHash,
                                    'timestamp' : str(self.timestamp),
                                    'nonce' : str(self.nonce)}),sort_keys=True)
        

# Calculate Block's Hash        
    def calculateHash(self):
        header = OrderedDict({ 'previousHash' : self.previousHash,
                                'timestamp' : str(self.timestamp),
                                'transactions' : str(self.transactions),
                                'nonce' : str(self.nonce) })
        header_json = json.dumps(header,sort_keys=True).encode('utf-8')
        return hashlib.sha256(header_json).hexdigest()

# Proof of Work
    def mineBlock(self):
        zerolist='0'
        while self.hash[0:self.difficulty] != zerolist*self.difficulty:
            self.nonce += 1
            self.hash = self.calculateHash()
        self.header = json.dumps(OrderedDict({ 'previousHash' : self.previousHash,
                                                'timestamp' : str(self.timestamp),
                                                'nonce' : str(self.nonce)}),sort_keys=True)
        print("BLOCK MINED:", self.hash)



