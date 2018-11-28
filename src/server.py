import hashlib

def hash_password(password):
    h = hashlib.md5()
    h.update(password.encode('utf-8'))
    return h.hexdigest()
