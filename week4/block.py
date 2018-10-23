import ecdsa
import hashlib
import json,random
from collections import OrderedDict


class Block(object):
    def __init__(self, timestamp, transactions, previousHash=''):
        self.timestamp = timestamp
        self.transactions = transactions
        self.merkle_root, self.generated_tree = self.build_tree(transactions)
        #print (self.merkle_root)
        #print (self.generated_tree)
        self.previousHash = previousHash
        self.nonce = 0
        self.difficulty=4
        self.hash = self.calculateHash()
        self.header = json.dumps(OrderedDict({ 'previousHash' : self.previousHash,
                                                'timestamp' : str(self.timestamp),
                                                'nonce' : str(self.nonce),
                                                'merkle_root' : str(self.merkle_root)}),sort_keys=True)
        
    def build_tree(self, past_transactions):
        """
        Builds merkle tree from self.past_transactions. Naive implementation of merkle tree as list of lists.
        :return: root of generated merkle tree
        """
        num_leaves = len(past_transactions)
        if num_leaves==0:
            return 0, []
        remaining_nodes = num_leaves
        generated_tree = []

        # Generate hashes for bottom layer
        leaf_hashes = []
        for transaction in past_transactions:
            new_hash = hashlib.sha256(transaction.json_msg.encode('utf-8')).hexdigest()
            leaf_hashes.append(new_hash)
        generated_tree.append(leaf_hashes)
        active_level = leaf_hashes

        while remaining_nodes != 1:
            if remaining_nodes % 2 == 0:
                odd = False
            else:
                odd = True
            new_tier = []
            for i in range(1, remaining_nodes, 2):
                combined_str = str(active_level[i-1]) + str(active_level[i])
                new_hash = hashlib.sha512(combined_str.encode('utf-8')).hexdigest()
                new_tier.append(new_hash)
            if odd:
                new_tier.append(active_level[num_leaves-1].encode('utf-8'))
            generated_tree.append(new_tier)
            remaining_nodes = len(new_tier)
            active_level = new_tier
        #print('Merkle tree build complete!\n' + 'No. of levels:', len(generated_tree))
        #print(generated_tree, '\n')
        return generated_tree[-1][0], generated_tree

    def proof_tree(self,transaction):
        #the transaction should be hashed
        path = []
        flag = False
        ti=0
        i=0
        if len(self.generated_tree)==0:
            return 0
        else:
            for index in self.generated_tree[0]:
                
                if str(index) == str(transaction):
                    flag=True
                    i=ti
                ti+=1
                
            if flag == False:
                return 0
            else:
                
                for index in self.generated_tree[:-1]:
                    # this is even
                    # left is 0, right is 1
                    if i % 2 ==0:
                        add_path=[1, index[i+1]]
                        path.append(add_path)
                    else:
                        add_path = [0, index[i-1]]
                        path.append(add_path)
                    i=int(i/2)
                    
                return path

# Calculate Block's Hash        
    def calculateHash(self):
        header = OrderedDict({ 'previousHash' : self.previousHash,
                                'timestamp' : str(self.timestamp),
                                'merkle_root' : str(self.merkle_root),
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
                                                'nonce' : str(self.nonce),
                                                'merkle_root' : str(self.merkle_root)}),sort_keys=True)
        print("\nBLOCK MINED:", self.hash)



