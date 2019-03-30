#source: https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/
import cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import database


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


def store_private_key(username):
    pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption())
    db = database.initialise_db("root", "Narnia0102*")
    query = "INSERT INTO private_keys VALUES ('" +  username + "', '" + str(pem) +  "');"
    print query
    database.query(query, db)



def store_public_key(username):

    pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo)
    file = str(username) + 'public_key.pem'
    with open(file, 'wb') as f:
        print pem
        f.write(pem)



def read_public_key(username):
    print "Currently in public key"
    global public_key
    file = str(username) + 'public_key.pem'
    with open(file, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )


def read_private_key(key_unprocessed):
    global private_key

    private_key = serialization.load_pem_private_key(
        key_unprocessed,
        password=None,
        backend=default_backend()
    )
    print "private key", private_key


def encrypt(message):
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None

        ))

    return encrypted

def decrypt(encrypted_message):
    global private_key
    original_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print original_message
    return original_message



