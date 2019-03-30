from bisect import bisect_left
import os
import pymongo
import time


def BinarySearch(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
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
                    res = BinarySearch(list, word)
                    if res != -1:
                        print("First occurrence of", word, "is present at", res)

    end = time.time()
    print "time elapsed", (end - start)

set_up('/home/nadia/Desktop/Third_Year_Project/t_file_200')
set_up('/home/nadia/Desktop/Third_Year_Project/t_files_400')
set_up('/home/nadia/Desktop/Third_Year_Project/t_files_500')
set_up('/home/nadia/Desktop/Third_Year_Project/t_files_600')
set_up('/home/nadia/Desktop/Third_Year_Project/t_files_800')
set_up('/home/nadia/Desktop/Third_Year_Project/t_fil_1000')
