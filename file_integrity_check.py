import os.path
import database
import hash
import Aho_Corasick
import track_new_file
import sys
import time


IS_FILE = 0
IS_DIR = 1
global response
response = 0
           
def is_file_or_dir(path):
    if(os.path.isfile(path)):
        return IS_FILE
    if(os.path.isdir(path)):
        return IS_DIR
    
def file_integrity(salt, hashed_password, username, file, db, DK, mode, mode2):

        checksum_new = hash.generate_file_checksum(file, DK)
        print "The DK is :",  DK
        print 'file is: ', file
        print "new checksum: " + str(checksum_new)
        query = "SELECT checksum FROM " + username + "_file_checksum WHERE ID = '" + file + "';"
        checksum_old = database.query_select(query, db)
        print 'The old checsum is: ', checksum_old
        #if the file does not exist in the database
        if(checksum_old == []):
            print 'The file does not exist'
            track_new_file.add_file_for_tracking(file)
            print 'The file has been added to the database'

        else:
            try:
                if(str(checksum_new) != str(checksum_old[0][0])):
                    #print file
                    print "file changed: suspicious"
                    #check file for virus

                    #virus check mode

                    if(mode == 1):
                        global response
                        response = Aho_Corasick.main(file, "none", 'none', DK)
                        if(response != None):
                            #print "xxx", response
                            return response
                            print "The response is: ", response
                            #Need to quarantine or deleted the file
                        elif(response == ""):
                            query = "UPDATE " + username + "_file_checksum SET checksum = '" + checksum_new + "' WHERE ID = '" + file + "';"
                            database.query(query, db)
                            query = "SELECT checksum FROM Nadia23_file_checksum WHERE ID = '" +  file + "';"
                            response  = database.query_select(query, db)
                            return 0
                    #-------------------------
                    #Integrity check mode
                    else:
                        changed_files = 1
                        #TODO save name of the changed file to a file called: changed_files
                        print 'changed file is: ', file
                        print "doing"
                        file2 = open('changed_files.txt', 'a')
                        file2.write(str(file) + " \n")
                        file2.flush()
                        file2.close()
                        return changed_files
                    #--------------------------
            except:
                 print "some error has occured"

        return 0



def main(path, username, mode, mode2):
    path = path.replace("'", "")
    query1 = "SELECT password FROM login WHERE username = '" + username + "';"
    query2 = 'SELECT salt FROM login WHERE username = \'' + username + "';"
    db = database.initialise_db("root", "Narnia0102*")
    hashed_password = database.query_select(query1, db)
    salt = database.query_select(query2, db)
    DK = hash.derive_secret_key(str(hashed_password), str(salt))
    response = file_integrity(salt, hashed_password, username, path, db, DK, mode, mode2)
    print 'res', response
    return response


# initialise()
start = time.time()
# main("/home/nadia/Desktop/Third_Year_Project/virus_checker_test", "Nadia23" )
end = time.time()
print("Time elapsed", (end - start))

