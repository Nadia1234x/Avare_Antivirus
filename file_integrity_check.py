import os.path
import mysql.connector
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

import time
import argon2
import hashlib
import sys
from subprocess import Popen, PIPE
import database
import email_alert
import check_fileExistence

import hash
import Aho_Corasick

IS_FILE = 0
IS_DIR = 1

           
def is_file_or_dir(path):
    if(os.path.isfile(path)):
        return IS_FILE
    if(os.path.isdir(path)):
        return IS_DIR
    
def file_integrity(salt, hashed_password, username, file, db, DK):
        checksum_new = hash.generate_file_checksum(file, DK)
        query = "SELECT checksum FROM " + username + "_file_checksum WHERE ID = '" + file + "';" 
        checksum_old = database.query_select(query, db)
        if(str(checksum_new) != str(checksum_old[0][0])):
            print file
            print "file changed: suspicious"
            #check file for virus 
            response = Aho_Corasick.main(file)
            if(response != ""):
                print response
                #Need to quarantine or deleted the file
            elif(response == ""):
                print "No viruses detected"
                query = "INSERT INTO " + username + "_file_checksum (ID) VALUES ('" + checksum_new + "');"
                database.query(query, db)

def main(path, username):
    
    query1 = "SELECT password FROM login WHERE username = '" + username + "';"
    query2 = "SELECT salt FROM login WHERE username = '" + username + "';"
    db = database.initialise_db("root", "Narnia0102*")
    hashed_password = database.query_select(query1, db)
    salt = database.query_select(query2, db)
    DK = hash.derive_secret_key(str(hashed_password), str(salt))
    response = is_file_or_dir(path)
    
    if(response == IS_FILE):
        file_integrity(salt, hashed_password, username, path, db, DK)
    if(response == IS_DIR):
        Aho_Corasick.initialise()
        for root, dirs, files in os.walk(path, topdown=False):
            for file in files:
                file = os.path.join(root, file)
                file_integrity(salt, hashed_password, username, file, db, DK) 

main("/home/nadia/Desktop/Third_Year_Project/", "Nadia23")
