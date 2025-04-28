import random
import string

def random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))