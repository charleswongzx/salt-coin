from collections import OrderedDict
from ecdsa import SigningKey, NIST192p, VerifyingKey
from datetime import datetime

import json, time, random, hashlib


class Transaction(object):

    def __init__(self, sender_public_key, receiver_public_key, amount, comment=''):
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.amount = amount
        self.comment = comment
        self.signature = ''

    def to_json(self):
        obj_dict = OrderedDict({'sender_public_key': self.sender_public_key,
                                'receiver_public_key': self.receiver_public_key,
                                'amount': self.amount,
                                'comment': self.comment})

        json_obj = json.dumps(obj_dict, sort_keys=True)

        return json_obj

    @classmethod
    def from_json(cls, json_obj):
        new_obj = json.loads(json_obj)
        return cls(new_obj['sender_public_key'], new_obj['receiver_public_key'], new_obj['amount'], new_obj['comment'])

    def sign(self, json_obj, private_key_string):
        sk = SigningKey.from_string(private_key_string, curve=NIST192p)
        signature = sk.sign(json_obj.encode('utf-8'))
        self.signature = signature
        return signature

    @staticmethod
    def validate(json_obj, signature, sender_public_key):
        vk = VerifyingKey.from_string(sender_public_key)
        return vk.verify(signature, json_obj.encode('utf-8'))

    def __eq__(self, other):
        # sign and compare? compare attributes one by one?
        return None


# sender_private = SigningKey.generate(curve=NIST192p)
# sender_public = sender_private.get_verifying_key()
#
#
# new = Transaction(sender_public.to_string().hex(), 'rofl', '50')
# test = new.to_json()
# sig = new.sign(test, sender_private.to_string())
# valid = Transaction.validate(test, sig, sender_public.to_string())
# print(valid)


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
        self.nonce = self.make_nonce()

        # Content
        self.past_transactions_tree = self.build_tree(past_transactions, verbose)  # Stored as a list

        # Generated hash
        self.hash = None  # Generated when inserted into chain
        # self.hash = self.generate_hash()  # to be generated upon adding to blockchain

    # def add_transaction(self, transaction):
    #     self.past_transactions.append(transaction)

    def build_tree(self, past_transactions, verbose):
        """
        Builds merkle tree from self.past_transactions. Includes naive implementation of merkle tree as list of lists.
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
            print('Tree build complete!\n' + 'No. of levels:', len(generated_tree))
            print(generated_tree)
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
        # Make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        header = OrderedDict({'version': self.version,
                              'index': self.index,
                              'previous_hash': self.previous_hash,
                              'timestamp': self.timestamp,
                              'merkle_root': self.merkle_root,
                              'nonce': self.nonce
                              })

        header_json = json.dumps(header).encode('utf-8')
        header_hash = hashlib.sha256(header_json).hexdigest()
        self.hash = header_hash
        return header_hash

    @staticmethod
    def make_nonce():
        """Generate pseudorandom number."""
        return str(random.randint(0, 100000000))


class Blockchain:
    def __init__(self):
        self.genesis_block = False
        self.current_block_number = 0

        self.chain = {}  # Arranged in hash: block key-value formatting
        self.previous_hash = None
        self.create_genesis()

    def create_genesis(self):
        """
        creates genesis block, adds to chain and sends 50 coins to recipient
        :recipient_address: mock address to send first txn
        :return: genesis Block object
        """
        if self.genesis_block:
            return 'Genesis already created!'

        genesis_transaction = Transaction('00000000000', '000000001', 50, 'Genesis transaction')
        previous_hash = 'genesis'

        block = Block([genesis_transaction])

        self.add_block(block)
        self.genesis_block = True

        return block

    def add_block(self, block, target_block_hash=None):
        """
        Assigns block a timestamp and index and adds to chain
        :param block: Block() object to be added
        :param target_block_hash: Used to assign block to another fork. Defaults to None for last used chain
        :return:
        """
        block.timestamp = time.time()
        block.index = self.next_block_number()
        block.generate_hash()

        self.chain[block.hash] = block

        if target_block_hash:
            block.previous_hash = target_block_hash
        else:
            block.previous_hash = self.previous_hash

        self.previous_hash = block.hash

        print('Block {} created in chain at {}'.format(block.index, datetime.utcfromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S')))
        print('Hash:', block.hash, '\n')

    def next_block_number(self):
        self.current_block_number += 1
        return self.current_block_number - 1

    # TODO: Get existing blocks
    # TODO: Save blocks to storage instead of memory


sender_private = SigningKey.generate(curve=NIST192p)
sender_public = sender_private.get_verifying_key()

tx1 = Transaction(sender_public.to_string().hex(), 'rofl', '50')
tx2 = Transaction(sender_public.to_string().hex(), 'lmao', '1000000')
tx3 = Transaction(sender_public.to_string().hex(), 'ded', '123')

transactions = [tx1, tx2, tx3]

block1 = Block(transactions)

salt_coin = Blockchain()

for i in range (10):
    salt_coin.add_block(block1)

print(salt_coin.chain)
