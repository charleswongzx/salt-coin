import hashlib

test_string = b"Blockchain Technology"

sha2_256_object = hashlib.sha256(test_string)
sha2_512_object = hashlib.sha512(test_string)
sha3_256_object = hashlib.sha3_256(test_string)
sha3_512_object = hashlib.sha3_512(test_string)

