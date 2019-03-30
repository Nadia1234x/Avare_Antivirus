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
    
def file_integrity(original_file ,salt, hashed_password, username, file, db, DK, mode, mode2):
        response = 0
        checksum_new = hash.generate_file_checksum(file, DK)
        query = "SELECT checksum FROM " + username + "_file_checksum WHERE ID = '" + original_file + "';"
        checksum_old = database.query_select(query, db)
        if(checksum_old == []):
            print 'The file does not exist'
            track_new_file.add_file_for_tracking(username, original_file, file)
            print 'The file has been added to the database'

        else:
            # try:
                if(str(checksum_new) != str(checksum_old[0][0])):
                    #print file
                    print "file changed: suspicious"
                    #check file for virus

                    #virus check mode

                    if(mode == "1"):
                        response = Aho_Corasick.main(username, original_file, file, "none", 'none', DK)
                        if(response != 0):
                            print "xxx", response
                            return response
                            print "The response is: ", response
                            #Need to quarantine or deleted the file
                        #if the file has been changed but if no viruses found

                        #response == "" changed to response == 0
                        #if no viruses have been found:
                        elif(response == 0):
                            query = "UPDATE " + username + "_file_checksum SET checksum = '" + checksum_new + "' WHERE ID = '" + original_file + "';"
                            database.query(query, db)
                            query = 'SELECT checksum FROM ' + username + '_file_checksum WHERE ID = "' +  original_file + '";'
                            print "in file_integrity check"
                            #print "The query is: ", query
                            response  = database.query_select(query, db)
                            return 0
                    #-------------------------
                    #Integrity check mode
                    else:
                        changed_files = 1
                        #TODO save name of the changed file to a file called: changed_files
                        #print 'changed file is: ', file
                        #print "doing"
                        if(username == 'Nadia32'):
                            file2 = open('changed_files.txt', 'a')
                        else:
                            file2 = open('changed_files2.txt', 'a')
                        file2.write(str(original_file) + " \n")
                        file2.flush()
                        file2.close()
                        return changed_files
                    #--------------------------
            # except:
            #      print "some error has occured"

        return 0



def main(original_file, path, username, mode, mode2):
    path = path.replace("'", "")
    query1 = "SELECT password FROM login WHERE username = '" + username + "';"
    query2 = 'SELECT salt FROM login WHERE username = \'' + username + "';"
    db = database.initialise_db("root", "Narnia0102*")
    hashed_password = database.query_select(query1, db)
    salt = database.query_select(query2, db)
    DK = hash.derive_secret_key(str(hashed_password), str(salt))
    response = file_integrity(original_file, salt, hashed_password, username, path, db, DK, mode, mode2)
    print 'res', response
    return response

# initialise()
start = time.time()
end = time.time()
print("Time elapsed", (end - start))

