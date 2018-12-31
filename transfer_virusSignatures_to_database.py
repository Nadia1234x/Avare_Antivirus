import database
import pymongo 

#transfer data to sql
#===============================================================================
# file_name = "main.mdb"
# db = database.initialise_db("root", "Narnia0102")
# file1 = open(file_name, "r")
# for line in file1: 
#     section_line = line.split(":")
#     virus_signature = section_line[1]
#     virus_name = section_line[2]
#     print section_line[1], section_line[2]
#     _query = "INSERT INTO virus_signatures VALUES('" +   virus_name + "', '" + virus_signature  + "');"
#     database.query(_query, db)
#===============================================================================

#===============================================================================
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
# 
# count = 1
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# database = client["HIDS"]
# collection = database["virus_signatures"]
# file_name = "main.mdb"
# file1 = open(file_name, "r")
# for line in file1: 
#         section_line = line.split(":")
#         virus_signature = section_line[1]
#         virus_name = section_line[2]
#         print section_line[1], section_line[2]
#         dictionary = {"name": virus_name, "signature": virus_signature}
#         insert = collection.insert_one(dictionary)
#         count = count + 1
#         if(count == 100000):
#             break
#         print count
#===============================================================================
