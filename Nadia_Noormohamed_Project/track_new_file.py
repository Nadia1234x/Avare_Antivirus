import os
import fnmatch
import hash
import database
#===============================================================================
# path = '/home/nadia/Desktop/'
# for filename in os.listdir(path):
#    print filename
#===============================================================================

 
 

# for root, dirs, files in os.walk("/home", topdown=False):
#    for file in files:
#         file = os.path.join(root, file)
#         if(os.path.isfile(file)):
def add_file_for_tracking(username, original_file, file):


    query1 = "SELECT password FROM login WHERE username = '" + username + "';"
    query2 = "SELECT salt FROM login WHERE username = '" + username + "';"
    db = database.initialise_db("root", "Narnia0102*")
    hashed_password = database.query_select(query1, db)
    salt = database.query_select(query2, db)
    print "yes"
    file_name = file
    DK = hash.derive_secret_key(str(hashed_password), str(salt))
    checksum = hash.generate_file_checksum(str(file_name), DK)
    print checksum
    query = "INSERT INTO " + username + "_file_checksum VALUES ('" + str(original_file) + "' ,'" +  checksum + "');"
    database.query(query, db)

# !/usr/bin/python
#===============================================================================
# 
# import os
# for root, dirs, files in os.walk("/home/nadia/Desktop/Third_Year_Project", topdown=False):
#    for name in files:
#       print(os.path.join(root, name))
#===============================================================================
   #============================================================================
   # for name in dirs:
   #    print(os.path.join(root, name))
   #============================================================================
