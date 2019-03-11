from collections import deque
import time
import pymongo
import deleteMalware
import socket




viruses_found = 0
    
output_function = []
number_of_states = 0
failure = []
concatenated_string = ""
FSM = []

client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["HIDS"]
collection = database["virus_signatures"]



#Obtain the hash of the malware free file and update on the database.


def build_structure():
    global FSM
    global output_function
    output_function = (32 * 10000) * [0]
    FSM = [[-1 for x in range(16)] for y in range(32 * 10000)] #sort this out!!



def build_FSM(word, word_char_list):

    global FSM
    #print "Starting Virus Detection..."
    global output_function

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
    return FSM
def complete_FSM(FSM):
       for alphabet in range(16):
        if(FSM[0][alphabet] == -1):
            FSM[0][alphabet] = 0



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
    global FSM
    output = current_state
    while(FSM[current_state][character] == -1):
        current_state = failure[current_state]
        FSM[current_state][character]
    return FSM[current_state][character]

#sets up       
def check_file(file_name, mode, mode2, DK):
    #mode is delete or quarantine
    #mode2 is test = 1 or acrual run = 0
    #The file that needs to be checked
    global viruses_found
    viruses_found = 0
    global concatenated_string
    concatenated_string = ""
    if(mode2 != 'test'):
        print "gfomgo"
        file2 = open(file_name.rstrip(), "r")

    else:
        print "fmfm"
        file2 = open(file_name, "r")


    try:
        open("infected_files.txt", 'w').close()
        #clears the file

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
            print 'The word is: ', word
            char_list = list(word)

            for x in range(len(char_list)):
                to_int_char = convert_alphaChar_to_int(char_list[x])
                if(to_int_char == "ignore"):
                    continue
                current_state = go_to_next_state(current_state, to_int_char)

                #print 'The current state for the character: ', char_list[x], 'from word: ', word, 'is: ', current_state

                if(output_function[current_state] != 0):
                    signature = output_function[current_state]
                    output = database.virus_signatures.find( { "signature":  str(signature)})


                    #put into method
                    for value in output:
                        print 'Test 1>>>>>>>>>', viruses_found
                        virus_name = str(value["name"])
                        print "found:" + virus_name
                        viruses_found = viruses_found + 1
                        #clear the file
                        result_file.write("file: " + str(file_name))
                        result_file.flush()
                        result_file2.write(str(file_name) + "\n")
                        result_file2.write(str(virus_name))
                        result_file2.flush()
                        result_file.write("found:" + str(virus_name) + "\n")
                        result_file.flush()
                        result_file.write("------ \n")
                        result_file.flush()
                        if(mode == "delete"):
                            print 'deleting'
                            deleteMalware.delete_virus(file_name.rstrip(), signature, DK)
                        concatenated_string = concatenated_string + virus_name + ""

    result_file.close()
    result_file2.close()
    if(mode2 == 'none'):
        return viruses_found
    if(mode2 == 'test'):
        return concatenated_string





  
def convert_alphaChar_to_int(char):
    try:
        number = int(char, 16)
        return number
    except:
        return "ignore"


def main(path, mode, mode2, DK):
    start = time.time()
    response = check_file(path, mode, mode2, DK)
    return response
    end = time.time()
    print(end - start)
