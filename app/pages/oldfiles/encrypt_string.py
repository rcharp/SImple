from simplecrypt import encrypt, decrypt
password = 'hyrule'

def encrypt_string(plaintext):

    ciphertext = encrypt(password, plaintext)
    encoded = ciphertext.encode('hex')
    return encoded

def decrypt_string(password, cipher):

    decoded = cipher.decode('hex')
    plaintext = decrypt(password, decoded)
    return plaintext
