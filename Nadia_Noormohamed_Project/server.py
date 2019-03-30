import socket
import sys
from threading import Thread
import check_login_details
import database
import file_integrity_check
import  Aho_Corasick
import hash
import AES_en_de
import time
import RSA
import register_user
import string
import random




#TCP connection
host = 'localhost'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 5555

try:
    s.bind((host, port))
except socket.error as e:
    print (str(e))

s.listen(5)
print('Waiting for a connection')
FSM = ''
file =''
nonce = ''
Aho_Corasick.initialisation()

def threaded_client(conn):
    conn.send(str.encode('Hello from server\n'))


    while True:
        data = conn.recv(2048)
        params = data.split("&-&")
        print params

        if(params[0] == 'file upload'):
            print "file upload------------------"
            global file
            if(params[2] == 'Nadia23'):
                file = 'file_to_scan_server'
            if(params[2] == "Nadia32"):
                file = 'file_to_scan_server_2'
            f = open(file, 'w')
            file_content = params[1]
            while "EOF" not in file_content:
                f.write(file_content)
                file_content = conn.recv(2048)
                print 'writing'
                print "file content is 1: ", file_content
            f.write(file_content)
            print "file content is 2: ", file_content
            print "finished writing"
            #conn.sendall('done')
            f.close()


            #replace the EOF character at the end of the file with "", as has not use anymore
            with open(file, 'r') as f:
                filedata = f.read()
            f.close()

            filedata = filedata.replace('EOF', "")

            with open(file, 'w') as f:
                f.write(filedata)
            f.close()

        if(params[0] == 'register'):
            print "in register server"
            username = params[1]
            password = params[2]
            response = register_user.check_username_availability(username, password)
            print response
            conn.send(str(response))


        if(params[0] == 'get-quarantine-files'):
            query = params[1]
            #print "query ", query
            db = database.initialise_db("root", "Narnia0102*")
            response = database.query_select(query, db)
            conn.send(str(response))

        if(params[0] == 'get-quarantine-file_path'):
            query = params[1]
            #print "query", params[1]
            db = database.initialise_db("root", "Narnia0102*")
            response = database.query_select(query, db)
            conn.send(str(response))





        #Testing
        if(params[0] == 'perform scan'):
            if(params[1] == "Nadia23"):
                thread2 = Thread(target = scan, args = (params, ))
                thread2.start()
                thread2.join()
            if(params[1]== "Nadia32"):
                thread3 = Thread(target = scan, args = (params, ))
                thread3.start()
                thread3.join()


        def scan(params):
            print "--------------performing scan"

            #transfer the input from file_to_scan_server to the original file name - do not have to do that.
            file1 = file
            original_file = params[4]

            print "The file being sent is: ", file, "for the original file, ", original_file
            viruses_found = file_integrity_check.main(original_file, file1, params[1], params[2], params[3])
           # print "The number of viruses found is: ", viruses_found
            conn.send(str(viruses_found))

        if(params[0] == 'delete-virus'):
            global db
            print "deleting the signatures from: ", file
            username = str(params[2])
            query1 = "SELECT password FROM login WHERE username = '" + str(username) + "';"
            query2 = 'SELECT salt FROM login WHERE username = \'' + str(username) + "';"
            db = database.initialise_db("root", "Narnia0102*")
            hashed_password = database.query_select(query1, db)
            salt = database.query_select(query2, db)
            DK = hash.derive_secret_key(str(hashed_password), str(salt))
            original_file = params[1]
            #print "The original file is: ", params[1]
            #calling function to delete the virus
            print "The file being sent is: ", file, "for the original file, ", original_file
            Aho_Corasick.check_file(username, original_file, file, "delete", "none", DK)
            #Sending the malware free file contents back to the client.

            #Send the file to the client.
            f = open(file, 'a')
            f.write('EOF')
            f.close()

            f = open(file, 'rb')
            file_content = f.read(2048)
            print "file_content", file_content

            while('EOF' not in file_content):

                conn.send(file_content)
            conn.send(file_content)

            f.close()
        def generate_nonce(length):
            return ''.join(random.choice(string.ascii_letters) for m in xrange(length))

        if(params[0] == "challenge"):
            print "Sending challenge"
            global nonce
            nonce = str(generate_nonce(32))
            conn.send(nonce)

        #validation of the login credentials
        if(params[0] == 'validate'):
            #generate challenge for the client

            print "currently validating"
            username = params[1]
            encrypted_password = params[2]
            #Need to decrypt the password first using the private key of the user.
            db = database.initialise_db("root", "Narnia0102*")
            query = "SELECT pr_key FROM private_keys WHERE username = '" + username + "';"
            key = database.query_select(query, db)
            print key
            print key[0][0]
            key = key[0][0]
            RSA.read_private_key(str(key))
            password = RSA.decrypt(encrypted_password)
            print password
            password, received_nonce = password.split("^^^")
            print "received nonce: ", received_nonce
            print 'nonce', nonce
            if(received_nonce == nonce):
                response = check_login_details.validate_credentials(str(username), str(password))
                conn.sendall(str(response))
            else:
                return False



        if(params[0] == 'logs'):
            query = params[1]
            db = database.initialise_db('root', 'Narnia0102*')
            response = database.query_select(query, db)
            print sys.getsizeof(response) * 8
            time.sleep(1)
            print "response is: ", response
            conn.sendall(str(response))

        #sets the user type to be a simple user.
        if(params[0] == 'set-simple'):
            print 'server set user to simple'
            query = params[1]
            db = database.initialise_db('root', 'Narnia0102*')
            database.query(query, db)


        if(params[0] == 'update_db_quarantine'):
            print "Server is updating the quarantine details"
            query = params[1]
            db = database.initialise_db("root", "Narnia0102*")
            database.query(query, db)
        #sets the user type to be advanced.
        if(params[0] == 'set-advanced'):
            print 'Server set the user to advanced'
            query = params[1]
            db = database.initialise_db('root', 'Narnia0102*')
            database.query(query, db)

        if(params[0] == 'get-number-scanned'):
            query = params[1]
            db = database.initialise_db('root', 'Narnia0102*')
            files_scanned = database.query_select(query, db)
            print "number of files scanned is: ", files_scanned
            conn.send(str(files_scanned))

        if(params[0] == 'new-day-first-scan'):
            print "no files scanned today, so inserting number of files scanned in first scan of day"
            query = params[1]
            db = database.initialise_db('root', 'Narnia0102*')
            database.query(query, db)

        if(params[0] == 'update-num-scanned-today'):
            print "updating the number of files scanned"
            query = params[1]
            db = database.initialise_db('root', 'Narnia0102*')
            database.query(query, db)

        if(params[0] == 'save-scan-details'):
            print "server is updating the details of scan just finished"
            query = params[1]
            db = database.initialise_db("root", "Narnia0102*")
            database.query(query, db)

        if(params[0] == 'Quarantine'):
            print "currently in quarantine"

            username = params[1]
            print "The username is: " + username
            AES_en_de.generate_key(username)
            out_file = 'test_encrypted_file.aes'
            AES_en_de.encrypt_file(file, out_file)
            #send the encypted file back to the client

            f = open(out_file, 'a')
            f.write('EOF')
            f.close()

            f = open(out_file, 'r')

            file_content = f.read(2048)
            print "file_content", file_content

            while('EOF' not in file_content):

                conn.send(file_content)
            conn.send(file_content)

            f.close()

        if(params[0] == 'decrypt-file'):
            'Decrypting file'
            print file

            print "currently in decrypt function"
            username = params[1]
            AES_en_de.generate_key(username)
            out_file = 'test_decrypted_file.aes'
            AES_en_de.decrypt_file(file, out_file)

            #Add EOF to decrypted file
            f = open(out_file, 'a')
            f.write('EOF')
            f.close()

            #Send the file to the client.
            f = open(out_file, 'r')

            file_content = f.read(2048)
            print "file_content", file_content

            while('EOF' not in file_content):

                conn.send(file_content)
            conn.send(file_content)

            f.close()

        if(params[0] == 'remove-from-quarantine-logs'):
            query = params[1]
            db = database.initialise_db("root", "Narnia0102*")
            database.query(query, db)






        if not data:
            break

    conn.close()

count = 0

while True:
    global count
    count = count + 1

    conn, addr = s.accept()
    print 'connected to: ' + addr[0] + ':' + str(addr[1])
    #Creating a thread for the connected client
    thread = Thread(target = threaded_client, args = (conn, ))
    print "connection is", conn
    count = count +1
    print count
    thread.start()

