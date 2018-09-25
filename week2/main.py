from ecdsa import SigningKey, NIST192p

from blockchain import Blockchain
from block import Block
from transaction import Transaction


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
    block1 = Block(transactions, verbose=True)
    salt_coin = Blockchain()

    for i in range (10):
        salt_coin.add_block(block1)

    print(salt_coin.chain)


if __name__ == '__main__':
    print('Running blockchain demo!')
    demo()
