import hashlib
import os
import time
import sys


def H(n, msg):
    n = int(n/8)
    return hashlib.sha512(msg).digest()[0:n]


def check_collision_time(bit_array_length):
    hashes_found = {}

    time_start = time.time()

    while True:
        rand_string = os.urandom(4)
        h = H(bit_array_length, rand_string)

        if h in hashes_found:
            v = hashes_found[h]
            if v == rand_string:  # same hash, but from the same source string
                continue
            else:
                time_end = time.time()
                print('Collision found!')

                return time_end - time_start

        hashes_found[h] = rand_string


def check_preimage_time(bit_array_length):
    time_start = time.time()

    x = b"\x00"

    while True:
        rand_string = os.urandom(4)
        h = H(bit_array_length, rand_string)

        if h == x:
            time_end = time.time()
            print('Preimage found for length', bit_array_length)

            return time_end - time_start


print(check_preimage_time(8))
print(check_preimage_time(16))
print(check_preimage_time(24))
print(check_preimage_time(32))
print(check_preimage_time(40))
