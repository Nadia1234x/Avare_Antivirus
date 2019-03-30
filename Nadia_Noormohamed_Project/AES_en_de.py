#The code for the encryption and decryption functions have been obtained from: https://pypi.org/project/pycrypto/
from Crypto.Cipher import AES
sizeOfBuffer  = 64 * 1024
import os, random, struct
import hash
import database
import random
import string

def generate_key(username):
    global key
    query2 = "SELECT salt FROM login WHERE username = '" + username + "';"
    db = database.initialise_db("root", "Narnia0102*")
    salt = database.query_select(query2, db)
    salt = salt[0][0]
    #TODO get the key of the user from the database.
    query = "SELECT AES_key FROM user_info WHERE user_name = '" + str(username) + "';"
    key = database.query_select(query, db)
    key = key[0][0]
    print key
    print type(key)
    key = hash.generate_password_hash(key, salt)
    print key
    #truncating the output to 32 bytes.
    key = key[:32]
    print key


key = ''



def encrypt_file(in_filename, out_filename, chunksize=64*1024):
    print "infile: ", in_filename
    print "outfile", out_filename

    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    global key
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    print key
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
    infile.close()
    outfile.close()

def decrypt_file(in_filename, out_filename, chunksize=24*1024):
    global key
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

# generate_key('none')
# encrypt_file(in_filename, out_filename)
# decrypt_file(out_filename, another_file)
