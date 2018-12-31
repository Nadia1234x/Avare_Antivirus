def create_stat_file():
    filename = raw_input("Please enter the name of the file to be tracked: ")
    stat_filename = filename + "_stat_.txt"
    f = open(stat_filename,'w') 
    f.write("stat file for " + filename)
    f.close()
    
create_stat_file()