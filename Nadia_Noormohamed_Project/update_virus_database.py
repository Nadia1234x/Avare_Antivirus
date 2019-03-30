import requests
import os
import time
import schedule
import pymongo
from datetime import date

def get_virus_file():
    print "doing"
    url = 'http://database.clamav.net/daily.cvd'
    request = requests.get(url)
    response_data =  request.content
    filename = "daily.cvd"
    file = open(filename, 'w')
    file.write(response_data)
    file.close()
    os.system('xxd -ps -s 512 daily.cvd|xxd -r -ps|tar -zx')
    os.system('chmod 764 daily.hdb')
    file = open("db-update.txt", "w ")
    today = str(date.today())
    file.write(today)


def update_database():

    count = 1
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["HIDS"]
    collection = database["virus_signatures"]
    collection.remove()
    file_name = "daily.hdb"
    file1 = open(file_name, "r")
    for line in file1:
             section_line = line.split(":")
             virus_signature = section_line[0]
             virus_name = section_line[2]
             print "virus signature: " + section_line[0], "virus name" + section_line[2]
             dictionary = {"name": virus_name, "signature": virus_signature}
             collection.insert_one(dictionary)
             count = count + 1
             if(count == 100000):
                 break
             print count

schedule.every().day.at("12:00").do(get_virus_file)
schedule.every().day.at("12:05").do(update_database)

while(1):
    schedule.run_pending()
    time.sleep(1)
    print "running"

