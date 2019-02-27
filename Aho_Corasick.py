from collections import deque
import time
import pymongo
import sys
import os.path
from pprint import pprint


    
output_function = []
number_of_states = 0
failure = []
concatenated_string = ""

client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["HIDS"]
collection = database["virus_signatures"]

def delete_virus(filename, signature):
    with open(filename, "rt") as file:
        file_contents = file.read()

    file_contents = file_contents.replace(signature, "<Removed>")

    with open(filename, 'w') as file:
        file.write(file_contents)





def build_FSM():
    print "Starting Virus Detection..."
    global output_function
    output_function = (32 * 1200) * [0]
    FSM = [[-1 for x in range(16)] for y in range(32 * 1200)] #sort this out!!

    #for developmement purposes only building a trie with 1000 signatures
    count = 0
    count_q = 0

    for word in collection.find({},{ "_id": 0, "name": 0}).limit(1000):
        count = count + 1.0
        count_q = count_q + 1
        print count
        percentage_complete = (count / 99000.0) * 100
        print percentage_complete, "% complete"
        word = word["signature"]
        word_char_list = list(word)
        current_state = 0

        for character in word_char_list:
            alphabet_num = convert_alphaChar_to_int(character)

            if(FSM[current_state][alphabet_num] == -1):
                global number_of_states
                number_of_states = number_of_states + 1
                FSM[current_state][alphabet_num] = number_of_states
                current_state = number_of_states
            else:
                current_state = FSM[current_state][alphabet_num]

    #for all character which do not have a transition from state 0
    #set the transtion to 0.
        output_function.insert(current_state, word)
    for alphabet in range(16):
        if(FSM[0][alphabet] == -1):
            FSM[0][alphabet] = 0

    return FSM


def failure_function_construction(FSM):
    #Each state except 0 has a f(state)
    global failure
    failure = [0] * number_of_states #sort out the 40
    queue = deque()
    #All states with a depth of 1 is 0 in the failure function
    for alphabet in range(16):
        if(FSM[0][alphabet] != 0):
            index = FSM[0][alphabet]
            failure.insert(index, 0)
            queue.append(index)

    current_state = queue.popleft()
    #While the queue does not become empty
    while(queue):
        for alphabet in range(16):
            if(FSM[current_state][alphabet] != -1):
                queue.append(FSM[current_state][alphabet])
                value = FSM[failure[current_state]][alphabet]
                #working out the failure fn of the transitions using alphabet that are successful
                failure[FSM[current_state][alphabet]] = value
        current_state = queue.popleft()


#uses go to and failure function. 
def go_to_next_state(current_state, character):  
    output = current_state
    while(FSM[current_state][character] == -1):
        current_state = failure[current_state]
        return FSM[current_state][character]
    return FSM[current_state][character]

#sets up       
def check_file(file_name, mode):

    #The file that needs to be checked
    global viruses_found
    global concatenated_string
    concatenated_string = ""
    file2 = open(file_name.rstrip(), "r")

    try:
        #clears the file
        #open("results_file.txt", "w").close()
        #Opens the file
        #Result for output result text box
        result_file = open("results_file.txt", "a")
        #Infected file names for listbox
        result_file2 = open("infected_files.txt", "a")
    except:
        print "cant open *****"
    for line in file2:
        word_list = line.split(" ")   
        for word in word_list:
            current_state = 0 
            word = word.rstrip()
            char_list = list(word) 
                       
            for x in range(len(char_list)):
                to_int_char = convert_alphaChar_to_int(char_list[x])
                if(to_int_char == "ignore"):
                    continue
                current_state = go_to_next_state(current_state, to_int_char)
    
                if(output_function[current_state] != 0): 
                    signature = output_function[current_state]
                    output = database.virus_signatures.find( { "signature":  str(signature)})
                    #put into method
                    for value in output:  
                        virus_name = str(value["name"])
                        print "found:" + virus_name
                        viruses_found = viruses_found + 1
                        result_file.write("file: " + str(file_name) + "\n")
                        result_file.flush()
                        result_file2.write(str(file_name) + "\n")
                        result_file.write("found:" + str(virus_name) + "\n")
                        result_file.flush()
                        result_file.write("------ \n")
                        result_file.flush()
                        if(mode == "delete"):
                            delete_virus(file_name.rstrip(), signature)
                        concatenated_string = concatenated_string + virus_name + ""
                        print "cs " + concatenated_string
    return viruses_found



    result_file.close()
    result_file2.close()
                  
  
def convert_alphaChar_to_int(char):
    try:
        number = int(char, 16)
        return number
    except:
        return "ignore"

viruses_found = 0
FSM = []
def initialise():
    global FSM
    FSM = build_FSM()
    failure_function_construction(FSM)


def main(path, mode):
    start = time.time()
    response = check_file(path, mode)
    return response
    end = time.time()
    print(end - start)

#For statistics

# def main(path):
#     count = 0
#     for root, dirs, files in os.walk(path, topdown=False):
#         start = time.time()
#         for file in files:
#             file = os.path.join(root, file)
#             count = count + 1
#             check_file(file)
#             if(count == 20):
#                 end = time.time()
#                 print(end - start)
#                 sys.exit()
#                 #return concatenated_string

# initialise()
# main("/home/nadia/Desktop/")
