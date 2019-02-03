from collections import deque
import time
import pymongo




from pprint import pprint



output_function = []
number_of_states = 0
failure = []
concatenated_string = ""
FSM = [[-1 for x in range(16)] for y in range(32 * 110000)] #sort this out!!

client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["HIDS"]
collection = database["virus_signatures"]

def convert_alphaChar_to_int(char):
    try:
        number = int(char, 16)
        return number
    except:
        return "ignore"


def build_FSM():
    print "Starting Virus Detection..."
    global output_function
    output_function = (32 * 100001) * [0]



    count = 0.0
    for word in collection.find({},{ "_id": 0, "name": 0}):
        count = count + 1.0
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

    return failure

FSM1 = []
def initialise():
    global FSM1
    FSM1 = build_FSM()

    failure_function_construction(FSM)

initialise()
