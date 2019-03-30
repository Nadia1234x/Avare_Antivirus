import os
import pymongo
import time


def linear_search(arr, x):

    for i in range(len(arr)):

        if arr[i] == x:
            return i

    return -1

def set_up(path):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["HIDS"]
    collection = database["virus_signatures"]
    start = time.time()
    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:

            file_name = os.path.join(root, file)
            f = open(file_name, 'r')
            for line in f:
                list = line.split(" ")
                list.sort()
                for word in collection.find({},{ "_id": 0, "name": 0}).limit(100000):
                    word = word["signature"]
                    res = linear_search(list, word)
                    if res !=-1:
                        print("First occurrence of", word, "is present at", res)

    end = time.time()
    print "time elapsed", (end - start)

set_up('/home/nadia/Desktop/Third_Year_Project/t_file_10')
set_up('/home/nadia/Desktop/Third_Year_Project/t_file')
