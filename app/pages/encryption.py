from Crypto.Cipher import AES
import base64
import os

# the block size for the cipher object; must be 16, 24, or 32 for AES
BLOCK_SIZE = 32

# set the secret key
secret = os.environ.get('SECRET_KEY')

def encode(plaintext):
    IV = Random.new().read(BLOCK_SIZE)
    aes = AES.new(secret, AES.MODE_CBC, IV)
    return base64.b64encode(aes.encrypt(plaintext))

def decode(encrypted):
    IV = Random.new().read(BLOCK_SIZE)
    aes = AES.new(secret, AES.MODE_CBC, IV)
    return aes.decrypt(base64.b64decode(encrypted))