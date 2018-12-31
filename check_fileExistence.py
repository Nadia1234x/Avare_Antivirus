import os.path
import mysql.connector 
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import time
import hashlib
import sys
from subprocess import Popen, PIPE
import database
import email_alert

def check_file_existence():
    with open("tracked_file.txt") as file:
            for line in file:
                #removing the white space after the line. 
                line = line.strip()
                result = os.path.isfile(line)
                if(result != True):
                    email_alert.send_alert(line)
                else:
                    print "The file does exist!"