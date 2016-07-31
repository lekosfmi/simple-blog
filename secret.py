import codecs
import string
import random

def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))

secret = codecs.encode(random_char(7), 'rot_13')
