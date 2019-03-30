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
	Aho_Corasick.initialisation()

def do_scan(file_path):
		print 'doing'
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
					response = Aho_Corasick.check_file('none', file, 'none', 'none', 'none')
		if(isFileResponse):
					file = file_path
					response = Aho_Corasick.check_file('none', file, 'none', 'none', 'none')
		end = time.time()
		print "time elapsed: " , end-start
		print count

test_set_up()

