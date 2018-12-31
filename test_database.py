import database 
import unittest
import hashlib


class test_database(unittest.TestCase):
    def test_database_initialisation(self):
        username = 'root'
        password = 'Narnia0102'
        assert database.initialise_db(username, password) != None 
        
    def test_if_database_insertion_passes(self):
        #test initialisation
        username = 'root'
        password = 'Narnia0102'
        db = database.initialise_db(username, password)
        hash_value = database.track_new_file_initialisation('/Users/nadianoormohamed/Desktop/Answers_to_SJT.docx', db, 'key')
        sql_query = "SELECT * FROM file_checksum WHERE ID = '" + hash_value + "';"
        response = database.query_select(sql_query, db)
        
        #testing if row is added
        assert str(response[0][0]) == hash_value
        assert response[0][1] == 1
        
        #delete row afterwards to prevent the table from getting too large
        sql_query = "DELETE FROM file_checksum WHERE ID = '" + hash_value + "';"
        database.query(sql_query, db)
        