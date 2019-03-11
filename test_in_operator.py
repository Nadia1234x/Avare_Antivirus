import pymongo
import time

import sys
import os.path



count = 0
start = time.time()
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["HIDS"]
collection = database["virus_signatures"]

def in_op():
    # This code is contributed by Bhavya Jain
    path = "/home/nadia/Desktop/Third_Year_Project/t_file_1000"
    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            file_name = os.path.join(root, file)
            try:
                file = open(file_name, "r")
                print count
                print file
                global count
                count = count + 1
                for line in file:
                    for word in collection.find({},{ "_id": 0, "name": 0}).limit(10000):
                        word = word["signature"]
                        if(word in line):
                            print True


            except:
                print "file does not exist"



            if(count == 999):
                end = time.time()
                print("time elapsed: " , (end-start))
                sys.exit()

in_op()
