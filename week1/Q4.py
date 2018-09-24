from ecdsa import SigningKey, NIST192p, VerifyingKey
import json
from collections import OrderedDict


class Transaction:

    @classmethod
    def new(cls, sender_public_key, receiver_public_key, amount, comment=''):
        cls.sender_public_key = sender_public_key
        cls.receiver_public_key = receiver_public_key
        cls.amount = amount
        cls.comment = comment

    def to_json(self):
        obj_dict = OrderedDict({'sender': self.sender_public_key,
                                'receiver': self.receiver_public_key,
                                'amount': self.amount,
                                'comment': self.comment})

        json_obj = json.dumps(obj_dict)

        return json_obj

    @classmethod
    def from_json(cls, json_obj):
        new_obj = json.loads(json_obj)
        cls.new(new_obj['sender_public_key'], new_obj['receiver_public_key'], new_obj['amount'], new_obj['comment'])

    def sign(self, json_obj, private_key_string):
        sk = SigningKey.from_string(private_key_string, curve=NIST192p)
        signature = sk.sign(json_obj)
        return signature

    def validate(self, json_obj, signature):
        vk = VerifyingKey.from_string(self.sender_public_key)
        return vk.verify(signature, json_obj)

    def __eq__(self, other):
        # sign and compare? compare attributes one by one?
        return None
