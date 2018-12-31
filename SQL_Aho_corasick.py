from collections import deque
import database
import time
import pymongo 



db = database.initialise_db("root", "Narnia0102")
output_function = []
number_of_states = 0
failure = []
            
def build_FSM():
    

            global output_function
            output_function = (32 * 100001) * [0] 
            print "wth is going on"
            FSM = [[-1 for x in range(16)] for y in range(32 * 110000)] #sort this out!!


            query = "SELECT signature FROM virus_signatures"
            response = database.query_select(query, db)
            for x in range(0, 100000):
                    word = response[x][0]
                    current_state = 0 
                    word_char_list = list(word)

                    
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
        #def build_output_function():
        
         
        #print "length", len(failure) 

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
def check_file(file_name):    
      #The file that needs to be checked
      
      file2 = open(file_name, "r")
      
      
      for line in file2:
          word_list = line.split(" ")   
                 
          for word in word_list:
              current_state = 0 
              #print "The word is", word
              word = word.rstrip()
              char_list = list(word) 
                         
              for x in range(len(char_list)):
                  to_int_char = convert_alphaChar_to_int(char_list[x])
                  if(to_int_char == "ignore"):
                      continue
                  current_state = go_to_next_state(current_state, to_int_char)

                  if(output_function[current_state] != 0):
                      signature = output_function[current_state]
                      query = "SELECT name FROM virus_signatures WHERE signature = '", signature, "';"
                      name = database.query_select(query, db)
                      print "found:", name
                  
                  
#methods converts alphabet to 0,...,25    
def convert_alphaChar_to_int(char):
    try:
        number = int(char, 16)
        return number
    except:
        return "ignore"

start = time.time()
FSM = build_FSM()    
failure_function_construction(FSM)
check_file("input_test_file_AC")
end = time.time()
print(end - start)





    