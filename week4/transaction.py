import json,random
from collections import OrderedDict
import ecdsa

class Transaction(object):
    def __init__(self, sender_public_key, receiver_public_key, amount):
        self.public_key = sender_public_key
        self.sender_public_key=sender_public_key.hex()
        self.receiver_public_key=receiver_public_key.hex()
        self.amount=amount
        self.nonce=random.getrandbits(32)
        self.signature=None
        self.json_msg = self.to_json()

    def to_json(self):
        obj_dict = OrderedDict({'sender_pk' : self.sender_public_key,
                                'receiver_pk' : self.receiver_public_key,
                                'amount' : self.amount,
                                'nonce' : self.nonce,
                                'signature' : self.signature })
        return json.dumps(obj_dict, sort_keys=True)
    
    def sign(self, json_obj, private_key_string):
        sk = ecdsa.SigningKey.from_string(private_key_string, curve=ecdsa.NIST192p)
        signature = sk.sign(json_obj.encode('utf-8'))
        self.signature = str(signature , 'utf-8' , 'ignore')
        self.json_msg=self.to_json()
        self.signature = signature


    def validate(self, json_obj, signature, sender_public_key):
        data=json.loads(json_obj)
        self.signature=None
        self.amount=data.get('amount')
        self.sender_public_key=data.get('sender_pk')
        self.receiver_public_key=data.get('receiver_pk')
        self.nonce=data.get('nonce')
        self.json_msg = self.to_json()
        vk = ecdsa.VerifyingKey.from_string(sender_public_key)
        validity=vk.verify(signature, self.json_msg.encode('utf-8'))
        self.signature = str(signature , 'utf-8' , 'ignore')
        self.json_msg=self.to_json()
        self.signature = signature
        return validity

