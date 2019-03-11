import Aho_Corasick
import pymongo
import time
import os


def determine_file_or_directory(file_path):
		#determining the type of the selected path.

		file_path = file_path.replace("'", "")
		isFileResponse = os.path.isfile(str(file_path))
		return isFileResponse

def test_set_up():
	client = pymongo.MongoClient("mongodb://localhost:27017/")
	database = client["HIDS"]
	collection = database["virus_signatures"]
	count = 0
	Aho_Corasick.build_structure()

	for word in collection.find({},{ "_id": 0, "name": 0}).limit(100000):
		word = word["signature"]
		word_char_list = list(word)
		FSM = Aho_Corasick.build_FSM(word, word_char_list)
	Aho_Corasick.complete_FSM(FSM)
	Aho_Corasick.failure_function_construction(FSM)

def do_scan(file_path):
		count = 0
		start = time.time()
		isFileResponse = determine_file_or_directory(file_path)
		if(isFileResponse == False):
			for root, dirs, files in os.walk(file_path, topdown=False):
				for file in files:
					file = os.path.join(root, file)
					count = count + 1
					print '------------------------------file being checked is: ', file
					#TODO this count will need to be changed because not all files can be opened
					#The scan is performed on the file.
					response = Aho_Corasick.check_file(file, 'none', 'none')
		if(isFileResponse):
					file = file_path
					response = Aho_Corasick.check_file(file, 'none', 'none')
		end = time.time()
		print "time elapsed: " , end-start
		print count

test_set_up()
do_scan('/home/nadia/Desktop/Third_Year_Project/t_file_1000/lorem_ipsum= (891st copy).txt')
