import database 
import argon2

def add_user(new_user, new_user_pass, admin_username, admin_password):
    db = database.initialise_db(admin_username, admin_password)
    query = "CREATE USER '" + new_user + "'@'localhost' IDENTIFIED BY '" + new_user_pass + "';"
    database.query(query, db)
    query = "USE HIDS;"
    database.query(query, db)
    query = "CREATE TABLE " + new_user + "_file_checksum( ID int, checksum VARCHAR(200));"
    database.query(query, db)
    query = "GRANT ALL ON HIDS." + new_user + "_file_checksum " + "TO '" + new_user + "'@'localhost';" 
    response = database.query(query, db)
   
    
admin_user = int(raw_input('Are you the admin? Enter 1 for Yes, 0 for No: '))
if(admin_user == 1):
    admin_user = raw_input('Please enter the admin username: ')
    admin_pass = raw_input('Please enter the admin password: ')
    new_user = raw_input('Please enter the new users username: ')
    new_user_pass = raw_input('Please enter the new users password: ')
    add_user(new_user, new_user_pass, admin_user, admin_pass) 
    
else: 
    "Please contact the admin at nadianoormohamed96@gmail.com to request account, specify the username and password in the email. Please make sure to change the password after the account has been created."
    

#What if the action fails, how can I let the user know. 
#Where is the password stored?     
 