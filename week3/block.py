from collections import OrderedDict

import json, random, hashlib


class Block(object):

    def __init__(self, past_transactions, verbose=False):
        """
        Initialisation of block
        :param past_transactions: list of transaction instances using Transaction() class
        """

        # Header
        self.version = '0.1-pre-alpha'
        self.index = None  # Applied when inserted into chain
        self.previous_hash = None  # Applied when inserted into chain
        self.timestamp = None  # Applied when inserted into chain
        self.merkle_root = None  # Assigned during build_tree() step
        self.nonce = random.getrandbits(32)  # Assigned once during creation, and again everytime miner attempts to rehash block
        self.target = 1.7e72  # can be converted into shorthand "bits" for space saving

        # Content
        self.past_transactions_tree = self.build_tree(past_transactions, verbose)  # Stored as a list

        # Generated hash
        self.hash = None  # Generated when inserted into chain

    def build_tree(self, past_transactions, verbose):
        """
        Builds merkle tree from self.past_transactions. Naive implementation of merkle tree as list of lists.
        :return: root of generated merkle tree
        """
        num_leaves = len(past_transactions)
        remaining_nodes = num_leaves
        generated_tree = []

        # Generate hashes for bottom layer
        leaf_hashes = []
        for transaction in past_transactions:
            new_hash = hashlib.sha256(transaction.to_json().encode('utf-8')).hexdigest()
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

        self.merkle_root = generated_tree[-1][0]

        if verbose:
            print('Merkle tree build complete!\n' + 'No. of levels:', len(generated_tree))
            print(generated_tree, '\n')
        return generated_tree

    def to_json(self):
        """
        Generate JSON string from block
        :return: JSON str
        """
        pass

    def generate_hash(self):
        """
        Create a SHA-256 hash of a Block object
        """
        self.generate_nonce()  # ensures every hash result is different

        # Make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        header = OrderedDict({'version': self.version,
                              'index': self.index,
                              'previous_hash': self.previous_hash,
                              'timestamp': self.timestamp,
                              'merkle_root': self.merkle_root,
                              'nonce': self.nonce,
                              'target': self.target
                              })

        header_json = json.dumps(header).encode('utf-8')
        header_hash = hashlib.sha256(header_json).hexdigest()
        self.hash = header_hash
        return header_hash

    def generate_nonce(self):
        """Generate pseudorandom number."""
        self.nonce = random.getrandbits(32)
