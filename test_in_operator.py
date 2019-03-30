import pymongo
import time

import sys
import os.path



count = 0

client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["HIDS"]
collection = database["virus_signatures"]

def in_op(path):
    # This code is contributed by Bhavya Jain
    start = time.time()
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
                    for word in collection.find({},{ "_id": 0, "name": 0}).limit(100000):
                        word = word["signature"]
                        if(word in line):
                            print True


            except:
                print "file does not exist"




    end = time.time()
    print count
    print("time elapsed: " , (end-start))




#in_op('/home/nadia/Desktop/Third_Year_Project/t_file')
in_op('/home/nadia/Desktop/Third_Year_Project/t_files_500')


