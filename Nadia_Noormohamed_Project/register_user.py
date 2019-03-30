import uuid
import database
import hash
import random
import string
import RSA

def check_username_availability(username, password):
    db = database.initialise_db("root", "Narnia0102*")
    query = "SELECT password FROM login WHERE username = '" + username + "';"
    result = database.query_select(query, db)
    if(result == []):
        print "The username does not exist"
        register_new_user(username, password, db)
    else:
        print "The username is taken"
        return False

    
def register_new_user(username, password, db):
    salt = uuid.uuid4()
    password_hashed = hash.generate_password_hash(password, str(salt))
    query = "INSERT INTO login (username, password, salt) VALUES ('" + username + "', '" + str(password_hashed) + "', '" + str(salt) + "');"
    print query
    database.query(query, db)
    query = "USE HIDS;"
    database.query(query, db)
    print 'username is', username
    username = username.encode('utf-8')
    query = "CREATE TABLE " + username + "_file_checksum (ID int, checksum VARCHAR(200));"
    print query
    database.query(query, db)
    #A new user is an advanced user by default + set key for qurantine functionality.
    key = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
    query = 'INSERT into user_info (user_name, user_type, AES_key) VALUES("' + str(username) + '", "' + 'advanced' + '", "' +  key + '");'
    database.query(query, db)
    #generate public private keys for the user:
    RSA.generate_keys()
    RSA.store_public_key(username)
    RSA.store_private_key(username)
    #Receive the public key file from the server
