import pymongo
import time

import sys
import os.path
# Following program is the python implementation of
# Rabin Karp Algorithm given in CLRS book

# d is the number of characters in the input alphabet
d = 256

# pat -> pattern
# txt -> text
# q -> A prime number

def search(pat, txt, q):
	M = len(pat)
	N = len(txt)
	i = 0
	j = 0
	p = 0 # hash value for pattern
	t = 0 # hash value for txt
	h = 1

	# The value of h would be "pow(d, M-1)%q"
	for i in xrange(M-1):
		h = (h*d)%q

	# Calculate the hash value of pattern and first window
	# of text
	try:
		for i in xrange(M):
			p = (d*p + ord(pat[i]))%q
			t = (d*t + ord(txt[i]))%q
	except:
		""

	# Slide the pattern over text one by one
	for i in xrange(N-M+1):
		# Check the hash values of current window of text and
		# pattern if the hash values match then only check
		# for characters on by one
		if p==t:
			# Check for characters one by one
			for j in xrange(M):
				if txt[i+j] != pat[j]:
					break

			j+=1
			# if p == t and pat[0...M-1] = txt[i, i+1, ...i+M-1]
			if j==M:
				print "Pattern found at index " + str(i)

		# Calculate hash value for next window of text: Remove
		# leading digit, add trailing digit
		if i < N-M:
			t = (d*(t-ord(txt[i])*h) + ord(txt[i+M]))%q

			# We might get negative values of t, converting it to
			# positive
			if t < 0:
				t = t+q
count = 0
start = time.time()
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["HIDS"]
collection = database["virus_signatures"]

# This code is contributed by Bhavya Jain
path = "/home/nadia/Desktop/"
for root, dirs, files in os.walk(path, topdown=False):
	for file in files:
		file_name = os.path.join(root, file)
		try:
			file = open(file, "r")
			print count
			print file
			count = count + 1
			for line in file:
				for word in collection.find({},{ "_id": 0, "name": 0}):
					word = word["signature"]
					search(word,line, 37)
		except:
			print "file does not exist"



		if(count == 20):
			end = time.time()
			print("time elapsed: " , (end-start))
			sys.exit()


