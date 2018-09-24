from ecdsa import SigningKey, NIST192p


test_string = b"Blockchain Technology"

sk = SigningKey.generate(curve=NIST192p)
vk = sk.get_verifying_key()

signature = sk.sign(test_string)

assert vk.verify(signature, test_string)




