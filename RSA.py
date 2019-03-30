#source: https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import database

private_key = ''
public_key = ''

def generate_keys():
    global private_key
    global public_key

    #----generation
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    print private_key
    public_key = private_key.public_key()
    print public_key


def store_private_key():

    pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption())


    with open('private_key.pem', 'wb') as f:
        f.write(pem)

def store_public_key():
    db = database.initialise_db("root", "Narnia0102*")
    pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo)

    with open('public_key.pem', 'wb') as f:
        print pem
        f.write(pem)



def read_public_key():
    global public_key
    with open("public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )


def read_private_key():
    global private_key
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
        print private_key

def encrypt():
    message = b'hello there'
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None

        ))
    print encrypted
    return encrypted

def decrypt(encrypted):
    original_message = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print original_message


##################
generate_keys()
store_private_key()
store_public_key()
encrypted = encrypt()
decrypt(encrypted)



