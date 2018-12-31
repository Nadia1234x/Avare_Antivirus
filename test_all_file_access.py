import os
import fnmatch
import hash
import database
#===============================================================================
# path = '/home/nadia/Desktop/'
# for filename in os.listdir(path):
#    print filename
#===============================================================================

query1 = "SELECT password FROM login WHERE username = 'Nadia23';"
query2 = "SELECT salt FROM login WHERE username = 'Nadia23';"
db = database.initialise_db("root", "Narnia0102*")
hashed_password = database.query_select(query1, db)
salt = database.query_select(query2, db)
 
 

for root, dirs, files in os.walk("/home", topdown=False):
   for file in files:
        file = os.path.join(root, file)
        if(os.path.isfile(file)): 
            file_name =  file
            print file_name
            print "yes"
            DK = hash.derive_secret_key(str(hashed_password), str(salt))
            checksum = hash.generate_file_checksum(str(file_name), DK)
            if(checksum == "error"):
                continue
            print checksum
            query = "INSERT INTO Nadia23_file_checksum VALUES ('" + str(file_name) + "' ,'" +  checksum + "');"
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