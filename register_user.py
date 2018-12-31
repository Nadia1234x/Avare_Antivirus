import uuid
import database
import hash 

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
    
    #create a new table for the user in the database 
    query = "CREATE USER '" + username + "'@'localhost' IDENTIFIED BY '" + str(password) + "';"
    database.query(query, db)
    query = "USE HIDS;"
    database.query(query, db)
    query = "CREATE TABLE " + username + "_file_checksum( ID int, checksum VARCHAR(200));"
    database.query(query, db)
    query = "GRANT ALL ON HIDS." + username + "_file_checksum " + "TO '" + username + "'@'localhost';" 
    response = database.query(query, db)
    

    
  