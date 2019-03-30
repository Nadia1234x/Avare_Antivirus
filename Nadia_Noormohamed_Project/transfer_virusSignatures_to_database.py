import database
import pymongo 

# count = 0
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# database = client["HIDS"]
# collection = database["virus_signatures"]
# for x in collection.find({},{ "_id": 0, "name": 0}):
#     count = count + 1
#     print count
#     print x["signature"]
#===============================================================================
# #===============================================================================
# #Used to add virus signatures to the mongodb database
def update_database():
    count = 1
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["HIDS"]
    collection = database["virus_signatures"]
    file_name = "daily.mdb"
    file1 = open(file_name, "r")
    for line in file1:
             section_line = line.split(":")
             virus_signature = section_line[1]
             virus_name = section_line[2]
             print section_line[1], section_line[2]
             dictionary = {"name": virus_name, "signature": virus_signature}
             insert = collection.insert_one(dictionary)
             count = count + 1
             if(count == 100000):
                 break
             print count
#===============================================================================
