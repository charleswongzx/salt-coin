from block import Block
from transaction import Transaction
import time
import json
import ecdsa

class Blockchain:
    def __init__(self):
        self.master_private_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST192p)
        self.master_public_key = self.master_private_key.get_verifying_key()
        self.genesis_private_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST192p)
        self.genesis_public_key = self.genesis_private_key.get_verifying_key()
        self.chain=[self.createGenesisBlock()]
        self.pendingTransaction=[]
        self.miningReward=100
        

    def createGenesisBlock(self):
        trans1 = Transaction(self.genesis_public_key.to_string(), self.master_public_key.to_string(),100000)
        pendingtransaction=[trans1]
        return Block("01/09/2018", pendingtransaction, "0")

    def getLatestBlock(self):
        return self.chain[len(self.chain)-1]

    def add (self, block, index, public_key):
        fork = False
        if len(self.chain) > index:
            fork = True
        check = checkvalidblock(block,index,fork)
        if check == True:
            for b in block:
                for trans in b.transactions:
                    if trans in self.pendingTransaction:
                        self.pendingtransaction.remove(trans)
            reward = Transaction( self.master_public_key.to_string(), public_key , self.miningReward * len(block))
            reward.sign(reward.json_msg, self.master_private_key.to_string())
            self.pendingtransaction.append(reward)
        if fork==True:
            resolve()
        
    def resolve(self):
        if len(self.chain[-1][0]) > len (self.chain[-1][1]):
            new_chain=self.chain[:-1]
            for i in self.chain[-1][0]:
                new_chain.append(i)
            self.chain = new_chain[:]

        if len(self.chain[-1][0]) < len (self.chain[-1][1]):
            new_chain=self.chain[:-1]
            for i in self.chain[-1][1]:
                new_chain.append(i)
            self.chain = new_chain[:]






