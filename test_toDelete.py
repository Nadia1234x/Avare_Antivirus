import database
from datetime import date
import datetime

# db = database.initialise_db('root', 'Narnia0102*')
# date = str(date.today())
# query = 'SELECT number FROM num_scanned_today WHERE date = "' + date + '";'
# number_scanned_db  = database.query_select(query, db)
#
# if(number_scanned_db == []):
#     query = 'INSERT INTO num_scanned_today (date, number) VALUES( "' + date + '"' + number_files_scanned_db + '" );'
#     database.query(query, db)
# else:
#     total_files_scanned_today = number_scanned_db + number_files_scanned_db
#     query = 'UPDATE number_scanned_today SET date = "' + date + '" number = "' + total_files_scanned_today + '" WHERE date = "' + date + '";'
db = database.initialise_db('root', 'Narnia0102*')
query = "SELECT * FROM scan_completed"
response = database.query_select(query, db)
print response[2]
response =  response[2]
print response[0]
print len(response)
#
# for x in range(len(response)):
#     for x1 in range(0, 4):
#      print response[0][x1]
