file_name = "test_go_to_fn"
file1 = open(file_name, "r")
for line in file1: 
        word_list = line.split(" ")
        print "the word list is: ", word_list
        for word in word_list:
            word = word.rstrip()
            print "The word 1 is: ", word
            
            word_char_list = list(word)
            print word_char_list