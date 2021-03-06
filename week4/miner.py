from block import Block
from transaction import Transaction
from collections import OrderedDict
import time
import json
import copy
import ecdsa

class Miner:
    def __init__(self, chain):
        self.chain = chain
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST192p)
        self.public_key = self.private_key.get_verifying_key()
        self.record_ledger = self.getChainLedger()
        self.verifiedTransactions=[]
        self.chain_check=False
        self.index=len(chain.chain) 
        self.selfish_index=len(chain.chain)    
        self.selfish_mine_count =0
        self.block_list=[]

# Mine class (Steps):
# 1. Check if chain is valid & Verify pool of pending Transactions
# 2. Create Block of Verified Transactions
# 3. Start Mining
# 4. Add block to chain upon successful mine
# 5. Update Miner's address:balance
# 6. Miner gets rewarded
    # Function to mine which mines the block and and updates the ledger and pushes changed to the chain
    def mine(self, pendingTransactions):
            if self.index<len(self.chain.chain) :
                self.record_ledger=self.getChainLedger()
                self.index=len(self.chain.chain)
            status=False
            block_list=[]
            print ("Verfiying Transcations")
            self.verifyTransaction(pendingTransactions)
            
            block = Block (time.time() , self.verifiedTransactions , self.chain.getLatestBlock().hash)
            #Proof-Of-Work
            block.mineBlock()
            print("++++++ BLOCK SUCESSFULLY MINED ++++++")
            block_list.append(block)
            status=self.chain.add(block_list, self.index, self.public_key.to_string())
            self.index +=1
   
            # Update record_ledger
            if status:
                self.record_ledger=self.getChainLedger()
            else:
                self.updateLedger(self.verifiedTransactions)
            self.verifiedTransactions=[]

    # Function to selfish mine which mines the block while not broadcasting the changes to the chain and only broadcasting the changes after mining a block first
    def selfish_mine(self, pendingTransactions):
            status=False
            if self.selfish_index ==1 :
                # self.selfish_index = copy.copy(self.index)
                self.selfish_index = len(self.chain.chain)
                self.record_ledger=self.getChainLedger()
            
            print ("\nSelfish Mining Is Underway")
            self.verifyTransaction(pendingTransactions)
            block = Block (time.time() , self.verifiedTransactions , self.chain.getLatestBlock().hash)
            #Proof-Of-Work
            block.mineBlock()
            self.selfish_mine_count += 1
            print("++++++ SELFISH BLOCK SUCESSFULLY MINED ++++++")
            self.block_list.append(block)
            self.updateLedger(self.verifiedTransactions)
            self.verifiedTransactions=[]
            if self.selfish_mine_count > 1:
                print ("Adding list of selfishly mined blocks to blockchain")
               
                status = self.chain.add(self.block_list, self.selfish_index, self.public_key.to_string())
                self.block_list=[]
                self.selfish_index +=1
                if status:
                    self.record_ledger=self.getChainLedger()

                #update record_ledger
                else:
                    self.updateLedger(self.verifiedTransactions)
                self.verifiedTransactions=[]

    # Update function is suppose to simulate a broadcast function in a network. 
    def update(self):
        self.record_ledger=self.getChainLedger()


# Miners should have the ability to send money to other miners
# Implement: new_transaction function
    def send_transaction(self, address, amount):
        transaction = Transaction(self.public_key.to_string(), address, amount)
        transaction.sign(transaction.json_msg, self.private_key.to_string())
        return transaction

# Verify Pending Transactions and add into list of verifiedTransactions
# We are verifying that there is enough balance in sender's wallet and that the transaction is signed aka trusted
    def verifyTransaction(self,transaction):
        copy_ledger = self.record_ledger.copy()
        currBal=0
        for trans in transaction:
            valid = trans.validate(trans.json_msg, trans.signature, trans.public_key)
            if valid ==True:
                if trans.sender_public_key in copy_ledger:
                    currBal = copy_ledger[trans.sender_public_key]
                else:
                    currBal=0
                    copy_ledger[trans.sender_public_key]=0

                if currBal >= trans.amount:
                    copy_ledger[trans.sender_public_key]-=trans.amount
                    self.verifiedTransactions.append(trans)


# Updates address-balance ledger after sucessfully mining block    
    def updateLedger(self,transaction):
        for trans in transaction:
            if trans.sender_public_key in self.record_ledger:
                self.record_ledger[trans.sender_public_key] = self.record_ledger[trans.sender_public_key]- trans.amount
            
            if trans.receiver_public_key in self.record_ledger:
                self.record_ledger[trans.receiver_public_key] += trans.amount
            else:
                self.record_ledger[trans.receiver_public_key] = trans.amount

# When a new miner is added it calculates the record ledger of the chain
# check record ledger dictionary if key of sender & receiver public key exist
# if it exist, add or subtract balance 
# if it does not exist create new key with value of 0
    def getChainLedger(self):
        record_ledger={}
        for block in self.chain.chain:
            for trans in block[0].transactions:
            	if trans.sender_public_key in record_ledger:
            		record_ledger[trans.sender_public_key] -= trans.amount
            	else:
            		record_ledger[trans.sender_public_key] = 0
            	
            	if trans.receiver_public_key in record_ledger:
            		record_ledger[trans.receiver_public_key] += trans.amount
            	else:
            		record_ledger[trans.receiver_public_key] = trans.amount
        return record_ledger


# Validation of Chain's Hash, Checks everytime we mine a block
    def chainvalidation(self):
        for i in range(1,len(self.chain)):
            currentBlock = self.chain [i]
            previousBlock = self.chain [i-1]
            if currentBlock.hash != currentBlock.calculateHash():
                return False
            if currentBlock.previousHash != previousBlock.hash:
                print(currentBlock.previousHash)
                print(previousBlock.hash)
                return False
        return True

    def getpath(self,transaction):
        for block in self.chain.chain:
            path = block[0].proof_tree(transaction)
            if path !=0:
                return path


