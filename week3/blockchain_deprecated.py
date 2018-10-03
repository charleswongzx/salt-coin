from ecdsa import SigningKey, NIST192p, VerifyingKey
from collections import OrderedDict

import json
import random
import time
import hashlib


class Transaction:

    def __init__(self, sender_public_key, receiver_public_key, amount, comment=''):
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.amount = amount
        self.comment = comment
        self.signature = ''

    def to_json(self):
        obj_dict = OrderedDict({'sender': self.sender_public_key,
                                'receiver': self.receiver_public_key,
                                'amount': self.amount,
                                'comment': self.comment})

        json_obj = json.dumps(obj_dict)

        return json_obj

    @classmethod
    def from_json(cls, json_obj):
        new_obj = json.loads(json_obj)
        return cls(new_obj['sender_public_key'], new_obj['receiver_public_key'], new_obj['amount'], new_obj['comment'])

    def sign(self, json_obj, private_key_string):
        sk = SigningKey.from_string(private_key_string, curve=NIST192p)
        signature = sk.sign(json_obj)
        self.signature = signature

    @staticmethod
    def validate(json_obj, signature, sender_public_key):
        vk = VerifyingKey.from_string(sender_public_key)
        return vk.verify(signature, json_obj)

    def __eq__(self, other):
        # sign and compare? compare attributes one by one?
        return None


class Block:
    # TODO: build tree every time new transaction is added

    def __init__(self):
        self.past_transactions = []
        self.past_transaction_hashes = []
        self.tiered_node_list = []
        self.root = None
        self.timestamp = time.time()
        self.nonce = self.make_nonce()
        self.block_number = None
        self.previous = None

    def add(self, new_transaction):
        new_hash_hex_digest = hashlib.sha512(new_transaction).hexdigest()
        self.past_transactions.append(new_transaction)
        self.past_transaction_hashes.append(new_hash_hex_digest)
        print('Added new transaction with hex digest:', new_hash_hex_digest)

    @staticmethod
    def make_nonce():
        """Generate pseudorandom number."""
        return str(random.randint(0, 100000000))

    def build(self):
        # Build tree computing new root
        num_leaves = len(self.past_transactions)
        remaining_nodes = num_leaves
        active_level = self.past_transaction_hashes

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
            self.tiered_node_list.append(new_tier)
            remaining_nodes = len(new_tier)
            active_level = new_tier

        self.tiered_node_list.insert(0, self.past_transaction_hashes)
        self.root = self.tiered_node_list[-1][0]
        print('Tree build complete!\n' + 'No. of levels:', len(self.tiered_node_list))

    def to_json(self):
        # Build tree and output to json
        self.build()
        block = {'block_number': self.block_number,
                 'previous': self.previous,
                 'timestamp': self.timestamp,
                 'transactions': self.past_transactions,
                 'root': self.root,
                 'nonce': self.nonce
                 }
        block_obj = json.dumps(block, sort_keys=True)
        return block_obj

    def add_block_number(self, number):
        self.block_number = number

    def add_previous_hash(self, previous_hash):
        self.previous = previous_hash

    def get_proof(self):
        # Get membership proof for entry
        pass

    def get_root(self):
        # Return the current root
        if not self.root:
            print('NO ROOT FOUND!\n' + 'Build new root using \'build\' method before calling \'get_root\'.')
            return None

        return self.tiered_node_list[-1][0]

    def verify_proof(entry, proof, root):
        # Verifies proof for entry and given root. Returns boolean.
        ...


class Blockchain:
    def __init__(self):
        self.genesis_block = False
        self.chain = OrderedDict()
        self.create_genesis('yo mommas house')
        self.previous_hash = ''

    def create_genesis(self, recipient_address):
        """
        creates genesis block, adds to chain and sends 50 coins to recipient
        :recipient_address: mock address to send first txn
        :return: genesis Block object
        """
        if self.genesis_block:
            return 'Genesis already created!'

        genesis_transaction = OrderedDict({'sender': "Author",
                                           'receiver': recipient_address,
                                           'amount': 50,
                                           'comment': "Genesis Transaction"})

        genesis_json = json.dumps(genesis_transaction, sort_keys=True).encode('utf-8')

        block = Block()
        block.add(genesis_json)
        block.add_block_number(1)
        block.add_previous_hash('00000')

        self.chain[self.hash(block.to_json())] = block
        self.genesis_block = True
        self.previous_hash = self.hash(block)

        return block

    def add_block(self, block, previous_hash=None):
        """
        Adds block to chain
        :param block: Block object to be added
        :return:
        """

        # TODO: add ability to select location to add block

        block.add_previous_hash(self.previous_hash)
        block.add_block_number()
        hash = self.hash(block.to_json())

        self.chain[hash] = block
        print('Block Added!')
        print('Block no.:', block.block_number)
        print('hash:', hash)

    def hash(self, block):
        """
        Create a SHA-256 hash of a Block object
        """
        # Make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = block.to_json()

        return hashlib.sha256(block_string).hexdigest()

    def resolve(self):
        """
        :return: latest block of the longest chain
        """
        pass



new_chain = Blockchain()
test_block = Block()
new_chain.add_block(test_block)
