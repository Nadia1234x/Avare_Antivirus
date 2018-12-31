import database

db = database.initialise_db("root", "Narnia0102")
signature = "9ac31bdfe490c015af9e2ef72265aeaf"
query = "SELECT name FROM virus_signatures WHERE signature = ", signature, ";"
response = database.query_select(query, db)
print response