import hashlib
import Aho_Corasick
import pymongo
import unittest
import random

class test_database(unittest.TestCase):
    database = ''
    collection = 0
    def test_Aho_Corasick_Setup(self):
        global database
        global collection
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        database = client["HIDS"]
        collection = database["virus_signatures"]
        Aho_Corasick.build_structure()
        for word in collection.find({},{ "_id": 0, "name": 0}).limit(10000):
                word = word["signature"]
                #print word["name"]
                word_char_list = list(word)
                FSM = Aho_Corasick.build_FSM(word, word_char_list)
        Aho_Corasick.complete_FSM(FSM)
        Aho_Corasick.failure_function_construction(FSM)

        file_name = "lorem_ipsum(1).txt"
        file = open(file_name,"a")
        file.close()
        for word in collection.find().limit(1):
            word = word["signature"]
        output = database.virus_signatures.find( { "signature":  str(word)})
        for value in output:
            signature_in_file = value['name']
        response = Aho_Corasick.check_file(file_name, 'none', 'test')
        print response
        if signature_in_file in response:
            assert True
        else:
            assert False







