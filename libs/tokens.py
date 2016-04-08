# coding=utf-8
__author__ = 'Sébastien Claeys'

import os, binascii, string, random

def generate_token():
    return binascii.hexlify(os.urandom(20)).decode()

def generate_password():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))