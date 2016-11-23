import base64
import os

from Crypto import Random
from Crypto.Cipher import AES

BS = 32
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]


class AESCipher:

    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc + "===")
        iv = enc[:32]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[32:] ))


cipher = AESCipher(os.environ.get('SECRET_KEY'))

def encode(plaintext):
    encrypted = cipher.encrypt(plaintext)
    return encrypted

def decode(encoded):
    decrypted = cipher.decrypt(encoded)
    return decrypted

"""
from Crypto.Cipher import AES
import base64
import os

# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 16

# set the secret key and the IV
secret = os.environ.get('SECRET_KEY')
IV = BLOCK_SIZE * '\x00'

# create a cipher object using the secret
cipher = AES.new(secret, AES.MODE_CBC, IV)

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = '{'

# one-liner to sufficiently pad the text to be encrypted
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

# one-liners to encrypt/encode and decrypt/decode a string
# encrypt with AES, encode with base64
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

def encode(plaintext):
    # encode a string
    #encoded = EncodeAES(cipher, plaintext)
    encoded = cipher.encrypt(plaintext)
    return encoded

def decode(encoded):
    # decode the encoded string
    #decoded = DecodeAES(cipher, encoded)
    decoded = cipher.decrypt(encoded)
    return decoded
"""