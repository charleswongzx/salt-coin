from ecdsa import SigningKey, NIST192p
from pprint import pprint
import time

from blockchain import Blockchain
from block import Block
from transaction import Transaction
from miner import Miner


def demo():

    # Getting sender pub and private keys
    sender_private = SigningKey.generate(curve=NIST192p)
    sender_public = sender_private.get_verifying_key()

    # Testing transaction signing and validation
    new = Transaction(sender_public.to_string().hex(), 'rofl', '50')
    test = new.to_json()
    sig = new.sign(test, sender_private.to_string())
    valid = Transaction.validate(test, sig, sender_public.to_string())
    print('Transaction validation:', valid)

    tx1 = Transaction(sender_public.to_string().hex(), 'rofl', '50')
    tx2 = Transaction(sender_public.to_string().hex(), 'lmao', '1000000')
    tx3 = Transaction(sender_public.to_string().hex(), 'test', '123')

    transactions = [tx1, tx2, tx3]

    salt_coin = Blockchain()
    miner1 = Miner(salt_coin)

    miner1.create_block(transactions)
    miner1.mine_block()


    # for i in range (10):
    #     salt_coin.add_block(block1)
    #     time.sleep(0.2)

    pprint(salt_coin.chain)


if __name__ == '__main__':
    print('Running blockchain demo!')
    demo()
