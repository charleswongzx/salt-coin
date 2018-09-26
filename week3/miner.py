from block import Block
import time


class Miner(object):
    def __init__(self, blockchain):
        self.target = None  # 256-bit number large enough to take miner 2-5s to solve, set when miner connects to network
        self.blockchain = blockchain  # chain assigned to miner
        self.active_block = None

    def create_block(self, transactions):
        self.active_block = Block(transactions)
        self.get_difficulty()

    def get_difficulty(self):
        self.target = self.active_block.target

    def mine_block(self):
        block_hash = 2**256-1  # max 256 bit number
        next_block_index = self.blockchain.current_block_number
        target = self.target

        while block_hash > target:
            self.active_block.timestamp = time.time()
            self.active_block.index = next_block_index
            self.active_block.previous_hash = self.blockchain.latest_hash
            block_hash = int(self.active_block.generate_hash(), 16)

        print('Block {} successfully mined!\n'.format(self.active_block.hash))

        if self.submit_block():
            self.active_block = None
            self.target = None



    def submit_block(self):
        self.blockchain.add_block(self.active_block)
        print('Block {} submitted to blockchain!'.format(self.active_block.hash))

    # looks at available transactions, sees how many txns fit into block
    # takes first k txns that fit, checks that they are signed and validated. if not signed or invalid, discard.
    # checks sender balance if they have sufficient coins
    # prevent double spending by nonce in Transaction class
    # adds transactions to block class
    # keeps hashing until hash < target


