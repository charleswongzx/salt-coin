from ecdsa import SigningKey, NIST192p, VerifyingKey
from collections import OrderedDict

import json


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
