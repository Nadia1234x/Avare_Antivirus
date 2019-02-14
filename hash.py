import argon2
import hashlib
import hmac

BUF_SIZE = 20
def generate_password_hash(password, salt):
    return hashlib.sha256(password + salt).hexdigest()

#Using HMAC
def generate_file_checksum(file, DK):
    print 'type is: ', type(file)
    digest = hmac.new(DK, ' ', hashlib.sha256)
    try:
        with open(file, 'r') as f: 
            while True: 
                data = f.read(BUF_SIZE)
                if not data:
                    break
                else: 
                    digest.update(data)
        digest = digest.hexdigest()          
        return digest
    except: 
        print "problem opening file"
        return "error"
    

#Not using HMAC. 
def generate_filePathName_checksum(path_name):
    hashed_path_name = hashlib.sha256(path_name)
    return hashed_path_name

def derive_secret_key(password, salt):
    # 1) Need to derive the key used to create file checksum so that the checksum 
    #can be re-found 
    iterations = 16
    memory_size = 8
    parallelism = 1
    buflen = 128
    derived_key = argon2.argon2_hash(password=password, salt=salt, t=iterations, m=memory_size, p=parallelism, buflen=128, argon_type=argon2.Argon2Type.Argon2_i)
    return derived_key
    #This is the file that does the integrity checking every hour
