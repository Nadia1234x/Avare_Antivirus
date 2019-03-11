import os.path
import mysql.connector 
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import time
import base64
import sys
import hash
from subprocess import Popen, PIPE
BUF_SIZE = 65536

#username = raw_input('Please enter your username:')
#password = raw_input('Please enter your password:')

def initialise_db(username, password):
    hids_database = mysql.connector.connect(user=username, password=password
    ,host='localhost',database='HIDS')
    return hids_database

# #Adds file into the db for the first time.
# def track_new_file_initialisation(file_hash, path_hash, db):
#     ID = path_hash
#     checksum = file_hash
#     sql_query = "INSERT INTO file_checksum VALUES('" + ID + "', '" + checksum + "');"
#     query(sql_query, db)
#     return hash_value
    
  
def query(sql_query, db):
    cursor = db.cursor()
    cursor.execute(sql_query)
    db.commit()
    #cursor.close()

#select queries return values.     
def query_select(sql_query, db):
    cursor = db.cursor()
    cursor.execute(sql_query)
    return cursor.fetchall()



