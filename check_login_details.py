import database
import hash 

def validate_credentials(username, input_password):
    
    db = database.initialise_db("root", "Narnia0102*")
    query = "SELECT salt FROM login WHERE username = '" + username + "';"
    salt = database.query_select(query ,db)
    salt = salt[0][0]
    hashed_password = hash.generate_password_hash(input_password, str(salt))
    query = "SELECT password FROM login WHERE username = '" + username + "';"
    password_obtained = database.query_select(query, db)
    print salt
    print "hash obtained:", password_obtained[0][0]
    print "hash generated:", hashed_password

    if(password_obtained[0][0] == hashed_password):
       print "You are logged in"
       #login_to_user_database_table(username, hashed_password)
       return True
    
def login_to_user_database_table(username, password):
    db = database.initialise_db(username, password)
    
    
    