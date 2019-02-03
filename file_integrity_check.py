import os.path
import database
import hash
import Aho_Corasick
import track_new_file
import sys
import time


IS_FILE = 0
IS_DIR = 1

           
def is_file_or_dir(path):
    if(os.path.isfile(path)):
        return IS_FILE
    if(os.path.isdir(path)):
        return IS_DIR
    
def file_integrity(salt, hashed_password, username, file, db, DK):
        checksum_new = hash.generate_file_checksum(file, DK)
        print "new checksum: " + str(checksum_new)
        query = "SELECT checksum FROM " + username + "_file_checksum WHERE ID = '" + file + "';" 
        checksum_old = database.query_select(query, db)
        print "old checksum: " +  str(checksum_old)
        print "P " + file
        try:
            if(str(checksum_new) != str(checksum_old[0][0])):
                print file
                print "file changed: suspicious"
                #check file for virus
                response = Aho_Corasick.main(file)
                if(response != ""):
                    print response
                    #Need to quarantine or deleted the file
                elif(response == ""):
                    print 'new checksum',  checksum_new
                    print "Old checksum",  checksum_old
                    print "No viruses detected"
                    query = "UPDATE " + username + "_file_checksum SET checksum = '" + checksum_new + "' WHERE ID = '" + file + "';"
                    database.query(query, db)
                    query = "SELECT checksum FROM Nadia23_file_checksum WHERE ID = '" +  file + "';"
                    response  = database.query_select(query, db)
                    print 'The checksum in the database is: ' , response
        except:
            print 'The file does not exist'
            track_new_file.add_file_for_tracking(file)
            print 'The file has been added to the database'



def main(path, username):
    
    query1 = "SELECT password FROM login WHERE username = '" + username + "';"
    query2 = "SELECT salt FROM login WHERE username = '" + username + "';"
    db = database.initialise_db("root", "Narnia0102*")
    hashed_password = database.query_select(query1, db)
    salt = database.query_select(query2, db)
    DK = hash.derive_secret_key(str(hashed_password), str(salt))
    count = 0

    response = is_file_or_dir(path)
    if(response == IS_FILE):
        file_integrity(salt, hashed_password, username, path, db, DK)
    if(response == IS_DIR):
        for root, dirs, files in os.walk(path, topdown=False):
            for file in files:
                file = os.path.join(root, file)
                # count = count + 1
                # if(count == 10):
                #     sys.exit()
                file_integrity(salt, hashed_password, username, file, db, DK)

def initialise():
    Aho_Corasick.initialise()


# initialise()
start = time.time()
# main("/home/nadia/Desktop/Third_Year_Project/virus_checker_test", "Nadia23" )
end = time.time()
print("Time elapsed", (end - start))

