import hashlib


class MerkleTree():

    def __init__(self):
        self.past_transactions = []
        self.past_transaction_hashes = []
        self.tiered_node_list = []
        self.root = None

    def add(self, new_transaction):
        new_hash_hex_digest = hashlib.sha512(new_transaction).hexdigest()
        self.past_transactions.append(new_transaction)
        self.past_transaction_hashes.append(new_hash_hex_digest)
        print('Added new transaction with hex digest:', new_hash_hex_digest)

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
        self.root = self.tiered_node_list[-1]
        print('Tree build complete!\n' + 'No. of levels:', len(self.tiered_node_list))

    def get_proof(self):
        # Get membership proof for entry
        pass

    def get_root(self):
        # Return the current root
        if not self.root:
            print('NO ROOT FOUND!\n' + 'Build new root using \'build\' method before calling \'get_root\'.')
            return None

        return self.tiered_node_list[-1]


def verify_proof(entry, proof, root):
    # Verifies proof for entry and given root. Returns boolean.
    ...


lol = MerkleTree()
lol.add(b'lol')
lol.add(b'laol')
lol.add(b'lodl')
lol.add(b'lols')
lol.add(b'lolz')
lol.add(b'lolc')
lol.add(b'lolf')
print(lol.past_transactions)
lol.build()
print(lol.get_root())

