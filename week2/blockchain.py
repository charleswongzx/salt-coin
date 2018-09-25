from transaction import Transaction
from block import Block

from datetime import datetime
import time


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
        Assigns block a timestamp, index, previous_hash and adds to chain.
        :param block: Block() object to be added.
        :param target_block_hash: Used to assign block to another fork. Defaults to None for last added block.
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
