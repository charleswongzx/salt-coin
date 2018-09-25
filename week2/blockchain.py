from collections import OrderedDict
from ecdsa import SigningKey, NIST192p, VerifyingKey

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

    # TODO: implement merkle generation, store root in self.root
    # header: previous_hash, index, merkle root, timestamp, nonce, block number, version
    # content: past transactions
    # self.hash is hash of the header

    def __init__(self, index, previous_hash, past_transactions, verbose=False):
        """
        Initialisation of block
        :param index: designated block number decided by order in which block is inserted into blockchain
        :param previous_hash: hash of previous block in chain
        :param past_transactions: list of transaction instances using Transaction() class
        """
        if verbose:
            print('Creating new block...')

        # Header
        self.version = '0.1-pre-alpha'
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.merkle_root = None  # Assigned during build_tree() step
        self.nonce = self.make_nonce()

        # Content
        self.past_transactions_tree = self.build_tree(past_transactions, verbose)  # Stored as a list

        # Generated hash
        self.hash = self.generate_hash()  # to be generated upon adding to blockchain

        print('Block', self.index, 'created at', self.timestamp)
        print('Hash:', self.hash)

    def add_transaction(self, transaction):
        self.past_transactions.append(transaction)

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
        self.chain = OrderedDict()
        self.create_genesis('yo mommas house')
        self.previous_hash = ''


sender_private = SigningKey.generate(curve=NIST192p)
sender_public = sender_private.get_verifying_key()

tx1 = Transaction(sender_public.to_string().hex(), 'rofl', '50')
tx2 = Transaction(sender_public.to_string().hex(), 'lmao', '1000000')
tx3 = Transaction(sender_public.to_string().hex(), 'ded', '123')

transactions = [tx1, tx2, tx3]

block1 = Block(0,'previous-hash', transactions)

