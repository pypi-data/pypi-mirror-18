import base64
import hashlib
import os
import re
from datetime import timedelta

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from Crypto.Cipher import DES


def _get_derived_key(password, salt, count):
    key = password + salt
    for i in range(count):
        m = hashlib.md5(key)
        key = m.digest()
    return key[:8], key[8:]


def encrypt(msg, password):
    if msg is None:
        return None
    salt = os.urandom(8)
    (dk, iv) = _get_derived_key(password, salt, 1000)
    crypter = DES.new(dk, DES.MODE_CBC, iv)
    # Pad plaintext per RFC 2898 Section 6.1
    padding = 8 - len(msg) % 8
    msg += chr(padding) * padding
    encrypted = salt + crypter.encrypt(msg)
    return encrypted.encode('base64')


def decrypt(msg, password):
    if msg is None:
        return None
    msg_bytes = base64.b64decode(msg)
    salt = msg_bytes[:8]
    enc_text = msg_bytes[8:]
    dk, iv = _get_derived_key(password, salt, 1000)
    crypter = DES.new(dk, DES.MODE_CBC, iv)
    text = crypter.decrypt(enc_text)
    # remove the padding at the end, if any
    return re.sub(r'[\x01-\x08]', '', text)


def generate_token(secret, expiration=timedelta(days=7), **token_data):
    expires_in = expiration.total_seconds() if isinstance(expiration, timedelta) else expiration
    s = Serializer(secret, expires_in=expires_in)
    return s.dumps(token_data).decode('ascii')


def parse_token(token, secret):
    s = Serializer(secret)
    if not token:
        return None
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    return data


def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Converts an integer to a base36 string."""
    if not isinstance(number, (int, long)) or number < 0:
        raise Exception('number must be a positive integer')

    base36 = ''

    if 0 <= number < len(alphabet):
        return alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return base36


def base36decode(number):
    return int(number, 36)


def signed_content(content, secret):
    m = hashlib.md5()
    m.update(secret)
    m.update(content)
    return m.hexdigest()
