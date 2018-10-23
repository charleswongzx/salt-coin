from blockchain import Blockchain
from block import Block
from miner import Miner
from transaction import Transaction
from SPVClient import Client
import json
from io import StringIO
import ecdsa


def demo():
    """
    #-----TESTING CODE PART 1-----
    # This still works
    # Getting sender public and private keys
    sender_private = ecdsa.SigningKey.generate(curve=ecdsa.NIST192p) 
    sender_public = sender_private.get_verifying_key()
    
    # Test code for Transaction
    new = Transaction(sender_public.to_string().hex(),'address2',50)
    test = new.json_msg
    sig = new.sign(test,sender_private.to_string())
    print(new.json_msg)
    valid = new.validate(test, sig, sender_public.to_string())
    print('Transaction Valid', valid)
    """

    """
    #-----TESTING CODE PART 2-----
    # This might not work anymore as some functions are moved from blockchain to miner class
    # Test Code for Blockchain & Block
    saltCoin = Blockchain()
    saltCoin.createTransaction(Transaction('address1', 'address2', 100))
    saltCoin.createTransaction(Transaction('address2','address1',50))
    
    print("Start miner")
    saltCoin.minePendingTransaction('miner-address')
    print("Balance(miner-address)", saltCoin.getBalanceofAddress('miner-address'))

    print("Start miner again")
    saltCoin.minePendingTransaction('miner-address')
    print("Balance(miner-address)", saltCoin.getBalanceofAddress('miner-address'))
    print("Balance(address1)", saltCoin.getBalanceofAddress('address1'))
    print("Balance(address2)", saltCoin.getBalanceofAddress('address2'))
    
    print ("Is chain valid?", saltCoin.chainvalidation())
    
    #Printing of Chain - To be used for SPV Client
    print ("\nSalt Coin Chain")
    i=0
    for block in saltCoin.chain:
        print ("\nBlock ", i, "Header: ")
        print (block.header)
        print ("Block ", i, "Hash: ")
        print (block.hash)
        print ("Block ", i, "Transactions: ")
        i+=1
        for trans in block.transactions:
            print (trans.json_msg)
    """

    """
    #-----TESTING CODE PART 3-----
    # May or Maynot work anymore
    # Testing miner class, without actual public keys
    pendingTransaction.append(transaction1)
    pendingTransaction.append(Transaction('','address1',100))
    pendingTransaction=[miner1.mine(pendingTransaction)]

    pendingTransaction=[miner1.mine(pendingTransaction)]
    
    pendingTransaction.append(Transaction(miner_public.to_string().hex(), 'address2', 50))
    pendingTransaction.append(Transaction(miner_public.to_string().hex(), 'address1',50))
    pendingTransaction=[miner1.mine(pendingTransaction)]
    
    pendingTransaction.append(Transaction('address1', 'address2', 5))
    pendingTransaction.append(Transaction('address2', 'address1',10))
    pendingTransaction=[miner1.mine(pendingTransaction)]

    print("Balance(miner-address)", miner1.record_ledger[miner_public.to_string().hex()])
    print("Balance(address1)", miner1.record_ledger['address1'])
    print("Balance(address2)", miner1.record_ledger['address2'])

    print ("\nSalt Coin Chain")
    i=0
    for block in saltCoin.chain:
        print ("\nBlock ", i, "Header: ")
        print (block.header)
        print ("Block ", i, "Hash: ")
        print (block.hash)
        print ("Block ", i, "Transactions: ")
        i+=1
        for trans in block.transactions:
            print (trans.json_msg)

    for key in miner1.record_ledger:
        print (key)
    """

    # Test Code for Miner Class with Key Pairs & signing of transactions
    client1=Client()
    client2=Client()
    saltCoin = Blockchain()
    miner1 = Miner(saltCoin)
    miner_m = Miner(saltCoin)

    # GENERATING LIST OF SIGNED TRANSACTIONS
    # trans1 is not meant to go through, based on the algo, both clients start with zero in their wallet
    trans1 = client1.send_transaction(client2.public_key.to_string(),100)
    # when block 1 is mined, miner gets a reward transaction which is added to wallet once block 2 is mined
    # therefore transaction 2 and 3 is the miner giving coins to the 2 clients
    trans2 = miner1.send_transaction(client1.public_key.to_string(),50)
    trans3 = miner1.send_transaction(client2.public_key.to_string(),50)
    # transaction 4 is the transaction between clients 
    trans4 = client1.send_transaction(client2.public_key.to_string(),10)

    saltCoin.pendingTransaction.append(trans1)
    miner1.mine(saltCoin.pendingTransaction)
    miner1.mine(saltCoin.pendingTransaction)
    saltCoin.pendingTransaction.append(trans2)
    

    miner1.mine(saltCoin.pendingTransaction)
    saltCoin.pendingTransaction.append(trans3)
    

    miner1.mine(saltCoin.pendingTransaction)

    miner1.mine(saltCoin.pendingTransaction)
    saltCoin.pendingTransaction.append(trans4)   

    miner1.mine(saltCoin.pendingTransaction)
    
    # Printing Chain and Block Header, Hash and Transactions
    print ("\nSalt Coin Chain")
    i=0
    for block in saltCoin.chain:
        print ("\nBlock ", i, "Header: ")
        print (block[0].header)
        print ("Block ", i, "Hash: ")
        print (block[0].hash)
        i+=1

    print ("\nBalance Ledger:")
    for key in miner1.record_ledger:
        print (key, miner1.record_ledger[key])
    
    # Printing of actual address-balance ledger this is for verification purposes, cos we can't really read the address key
    print("\nBalance(miner-address)", miner1.record_ledger[miner1.public_key.to_string().hex()])
    print("Balance(address1)", miner1.record_ledger[client1.public_key.to_string().hex()])
    print("Balance(address2)", miner1.record_ledger[client2.public_key.to_string().hex()])

    # Test for SPV client receive transaction function
    # return True if transaction is in chain
    print(client1.receive_transaction(trans4, miner1))
    print(client1.receive_transaction(trans1, miner1))
    print(client1.receive_transaction(trans2, miner1))
    print(client1.receive_transaction(trans3, miner1))



if __name__ == '__main__':
    print('Running blockchain demo!')
    demo()