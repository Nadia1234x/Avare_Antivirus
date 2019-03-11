from Tkinter import *
import check_login_details
import tkFileDialog
import register_user
import file_integrity_check
from tkMessageBox import showinfo, showerror
import os
import Aho_Corasick
import update_virus_database
from datetime import date
import ttk
import time
from decimal import Decimal
import math
import pyaes
count = 0
import database
from datetime import date
import datetime
import pymongo
import hash
import socket
import sys

PORT = 5555


try:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

print('connecting to the server')
s.connect(('localhost', 5555))

#Send data

try:
    s.sendall('hello')
except socket.error:
    sys.exit()

#Receive data
reply = s.recv(4096)
print reply



#
# def quarantine_file():
#     output = pyaes.AESModeOfOperationCBC(key)

def delete_malare_simple_user():
    global window2
    global filePath
    window2.configure(background = "Black")
    window2.title('Results')
    window2.configure('200x200')
    progressBar.destroy()
    pause_button.destroy()
    resume_button.destroy()
    percentage_complete_label.destroy()
    found_malware.destroy()
    scanned_files.destroy()
    found_malware.destroy()
    found.destroy()
    current_files_scanning.destroy()
    number_of_files_scanned.destroy()
    scanning.destroy()
    next.destroy()



    malware_deleted_label = Label(window2, text = 'All files have been deleted!')
    malware_deleted_label.configure(background = 'black', fg = 'white')
    malware_deleted_label.place(relx = 0.30, rely = 0.30)

    count = 1
    file = open('infected_files.txt', 'r')
    for line in file:
        if(line != "\n"):
            if(count % 2 != 0):
                filePath = str(line)
                count = count + 1
                print filePath
                delete_virus()
    file.close()







def user_fn():
    print advanced_user.get()
    print simple_user.get()
    if(advanced_user.get() == True):
        user = 'advanced'
        print 'Advanced User'
        db = database.initialise_db('root', 'Narnia0102*')
        query = 'SELECT user_type FROM user_info WHERE user_name = "'  + username.get() + '" ;'
        response = database.query_select(query, db)
        if(response == []):
            query = 'INSERT INTO user_info (user_name, user_type) VALUES ("' + username.get() + '" , "' +  user + '");'
            database.query(query, db)
        else:
            query = 'UPDATE user_info SET user_name = "' + username.get() + '" , user_type = "' + user + '" WHERE user_name = "' + username.get() + '";'
            database.query(query, db)
    if(simple_user.get()== True):
        user = 'simple'
        print 'Simple User'
        db = database.initialise_db('root', 'Narnia0102*')
        query = 'SELECT user_type FROM user_info WHERE user_name = "'  + username.get() + '" ;'
        response = database.query_select(query, db)
        if(response == []):
            query = 'INSERT INTO user_info (user_name, user_type) VALUES ("' + username.get() + '" , "' +  user + '");'
            database.query(query, db)
        else:
            query = 'UPDATE user_info SET user_name = "' + username.get() + '" , user_type = "' + user  + '" WHERE user_name = "' + username.get() + '";'
            database.query(query, db)

def delete_virus():
    global user_type
    file_name = filePath
    print file_name
    username = "Nadia23"
    query1 = "SELECT password FROM login WHERE username = '" + username + "';"
    query2 = 'SELECT salt FROM login WHERE username = \'' + username + "';"
    db = database.initialise_db("root", "Narnia0102*")
    hashed_password = database.query_select(query1, db)
    salt = database.query_select(query2, db)
    DK = hash.derive_secret_key(str(hashed_password), str(salt))

    Aho_Corasick.check_file(file_name, "delete", "none", DK)

    if(user_type == 'advanced'):
        print 'id: ', current_item_identifier
        treeview.set(current_item_identifier, 'Action Taken', 'Deleted')
        treeview.update()

def quarantine_file():
    print 'id: ', current_item_identifier
    treeview.set(current_item_identifier, 'Action Taken', 'Quarantined')
    treeview.update()




def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

#TODO calculate the total bytes of the files to be scanned, then as each file is scanned, obtain the number of bytes of that file and calculate the percentage.

def initialise_scanning():
    global times_initialised
    times_initialised= times_initialised + 1
    global progressBar2

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    database = client["HIDS"]
    collection = database["virus_signatures"]
    count = 0
    Aho_Corasick.build_structure()

    for word in collection.find({},{ "_id": 0, "name": 0}).limit(10000):
        count = count + 1.0
        print count
        percentage_complete = (count / 10000.0) * 100

        progressBar2['value'] = percentage_complete
        progressBar2.update()
        print percentage_complete, "% complete"
        #increase_progress_bar(percentage_complete)
        word = word["signature"]
        word_char_list = list(word)
        FSM = Aho_Corasick.build_FSM(word, word_char_list)
    Aho_Corasick.complete_FSM(FSM)
    Aho_Corasick.failure_function_construction(FSM)


def get_number_of_files_scanned():
    db = database.initialise_db('root', 'Narnia0102*')
    date_scanned = str(date.today())
    query = 'SELECT number FROM num_scanned_today WHERE date = "' + date_scanned + '";'
    files_scanned = database.query_select(query, db)
    if(files_scanned == []):
        return '0'
    return str(files_scanned[0][0])


def update_num_files_scanned(number_files_scanned):
    global number_of_files_scanned_today
    db = database.initialise_db('root', 'Narnia0102*')
    date_scanned = str(date.today())
    query = 'SELECT number FROM num_scanned_today WHERE date = "' + date_scanned + '";'
    number_scanned_db  = database.query_select(query, db)
    print "db returned: ", number_scanned_db

    if(number_scanned_db == []):
        query = 'INSERT INTO num_scanned_today (date, number) VALUES( "' + date_scanned + '", "' + str(number_files_scanned) + '" );'
        database.query(query, db)
        number_of_files_scanned_today['text'] = number_files_scanned
        number_of_files_scanned_today.update()
    else:
        number_scanned_db = number_scanned_db[0][0]
        total_files_scanned_today = number_scanned_db + number_files_scanned
        query = 'UPDATE num_scanned_today SET date = "' + date_scanned + '", number = "' + str(total_files_scanned_today) + '" WHERE date = "' + date_scanned + '";'
        database.query(query, db)
        number_of_files_scanned_today['text'] = str(total_files_scanned_today)
        number_of_files_scanned_today.update()


def scan():
        print  "---------------------------------------------8"
        global percentage_complete
        percentage_complete = 0
        global total
        total = 0
        global number_of_files
        number_of_files = 0
        #for malware scan
        global number_of_viruses_found
        number_of_viruses_found = 0
        #for integrity_scan
        global number_of_changed_files
        number_of_changed_files = 0
        global count_files
        count_files = 0;

        #---

        if(scanning_mode == 1):
            open("infected_files.txt", "w").close()
        if(scanning_mode == 0):
            open("changed_files.txt", "w").close()


        isFileResponse = determine_file_or_directory()
        iterate_files(isFileResponse)

        #TODO change this later so that the final number rounds to 100
        global current_files_scanning
        current_files_scanning['text'] = 'Scan complete'
        create_scan_finished_button()

        #save details of the scan for the log information
        save_scan_details()
        #save the number of viruses scanned today
        update_num_files_scanned(count_files)
        #reset number for the next scan
        number_of_viruses_found = 0



def save_scan_details():
       #save the details of the virus scan to the database for the log page
        if(scanning_mode == 1):
            scan_type = "Malware Scan"
        else:
            scan_type = "Integrity Scan"
        date_time = datetime.datetime.now()
        time = date_time.strftime("%I:%M:%S %p")
        print 'time of scan', time
        scan_date = str(date.today())
        print 'date of scan', scan_date
        db = database.initialise_db('root', 'Narnia0102*')
        query = 'INSERT INTO scan_completed(path, malware_count, date, time, scan_type) VALUES ( "'+ str(file_path) + '" , "'+ str(number_of_viruses_found) + '", "' +  str(scan_date) + '" , "' + time +'", "' + scan_type + '" );'
        database.query(query, db)


def determine_file_or_directory():
        #determining the type of the selected path.
        global file_path
        file_path = file_path.replace("'", "")
        isFileResponse = os.path.isfile(str(file_path))
        return isFileResponse

def iterate_files(isFileResponse):
      start = time.time()
      global count_files
      if(isFileResponse == False):
            for root, dirs, files in os.walk(file_path, topdown=False):
                for file in files:
                    file = os.path.join(root, file)
                    #TODO this count will need to be changed because not all files can be opened
                    count_files = count_files + 1;
                    #The scan is performed on the file.
                    perform_scan(file)
      if(isFileResponse):
                    file = file_path
                    perform_scan(file)
                    count_files = count_files + 1;
      end = time.time()
      print "time elapsed: " , end-start


#--TODO Refactor this method.
def perform_scan(file):
    global number_of_viruses_found
    global percentage_complete
    global total
    global number_of_files
    total_files_size = calculate_file_bytes()
    global scanning_mode
    global number_of_changed_files


    response = file_integrity_check.main(file, 'Nadia23', scanning_mode, 'none')
    print 'The response is',  response


    if(scanning_mode == 1):
        number_of_viruses_found = number_of_viruses_found + response
        found_malware['text'] = number_of_viruses_found
        #number_of_viruses_found
        found_malware.update()

    if(scanning_mode == 0):
        number_of_changed_files = number_of_changed_files + response
        changed_files['text'] = number_of_changed_files
        changed_files.update()

    #Logic to increment the progress bar
    current_file_size = os.path.getsize(file)
    total = total + current_file_size
    number_of_files = number_of_files + 1
    percentage_complete = percentage_complete + ((Decimal(current_file_size)/Decimal(total_files_size)) * 100)
    print str(percentage_complete) + ' %'
    global percentage_complete_label
    percentage_complete_label['text'] = str(percentage_complete) + '% complete'
    #increase the progress bar depending on how many bytes of files have been scanned.
    inc_progress_bar(percentage_complete)

    #Displays the current number of files scanned and the current files being scanned
    current_files_scanning['fg'] = 'white'
    current_files_scanning['text'] = str(file)
    global number_of_files_scanned
    number_of_files_scanned['text'] = str(number_of_files)
    number_of_files_scanned.update()
    current_files_scanning.update()


def calculate_file_bytes():
      total = 0
      global file_path
      file_path = file_path.replace("'", "")
      if(os.path.isdir(str(file_path))):
          for root, dirs, files in os.walk(str(file_path), topdown=False):
                for file in files:
                    try:
                        file = os.path.join(root, file)
                        total = total + os.path.getsize(file)
                    except:
                        continue
      else:
          total = os.path.getsize(str(file_path))
      return total




def update_datatbase():
    update_virus_database.get_virus_file()
    update_virus_database.update_database()
    Date = str(date.today())
    # last_update = Label(config_window, text = Date)
    # last_update.configure(background = 'White', fg = 'Green')
    # last_update.place(relx = 0.13, rely = 0.56)
    date_update['text'] = Date
    date_update['fg'] = 'Green'
    print Date

def Select_from_listbox(event):
    global value
    value = listbox.get(ANCHOR)
    print value

def raise_frame(frame):
    frame.tkraise()


def save_login_details(event):
    global s
    global username1
    username1 = username.get()
    password1 = password.get()
    response = check_login_details.validate_credentials(str(username1), str(password1))
    s.sendall('check credentials')
    if(response == True):
        showinfo("login success", "You have successfully logged in")
        raise_frame(f6)
        get_test()


def hide(event):
    event.widget.pack_forget()

def open_file_browser(event):
    global file_path
    file_path = tkFileDialog.askopenfile(mode = 'r',  initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    file_path = str(file_path).split(",")
    file_path =  file_path[0]
    file_path = file_path.split(" ")
    file_path =  file_path[2]
    print file_path

def open_directory_browser(event):
    global file_path
    file_path = tkFileDialog.askdirectory(initialdir = "/", title = 'Select Directory')

def register_new_user(event):
    username = new_username.get()
    password = new_password.get()
    password_re = re_new_password.get()
    if(password == password_re):
        response = register_user.check_username_availability(username, password)
        print response
        if(response == False):
            username_taken = showerror("Password Error", "Username taken: Please choose another username.")

    else:
        showerror("Error", "Password Error: Passwords do not match")

def show_password():
    print "worked!"
    print show_pass.get()
    if(show_pass.get() == True):
        reg_password_entry_path.config(show = '')
        re_reg_password_entry_path.config(show = '')

    else:
        reg_password_entry_path.config(show = '*')
        re_reg_password_entry_path.config(show = '*')

def increase_progress_bar(percentage):
    progressBar2['value'] = percentage
    progressBar2.update()

def create_malware_results_treeview():
    window2.configure(background = 'black')
    global treeview
    treeview = ttk.Treeview(window2)
    style = ttk.Style(window2)
# set ttk theme to "clam" which support the fieldbackground option
    style.theme_use("clam")
    style.configure("Treeview", background="#4a3cc4", fieldbackground="#4a3cc4", foreground="white")
    treeview.column('#0', width = 260)
    treeview.heading('#0', text = 'Infected File')
    treeview.config(columns = ('File Path', 'Malware', 'Action Taken'))
    treeview.heading('File Path', text = 'File Path')
    treeview.heading('Malware', text = 'Malware Found')
    treeview.heading('Action Taken', text = 'Action Taken')
    treeview.column('Malware', width = 230)
    treeview.bind('<<TreeviewSelect>>', callback)

    item_count = 0
    line_count = 1
    count = 10
    file = open("infected_files.txt")
    current_file = ''
    for line in file:
         file_path = str(line)
         if((line_count % 2) != 0): #if a filename
             line = line.split('/')
             file_name = line[-1]
             #if(current_file != file_name):
             position = str(item_count)
             identifier = 'item' + str(item_count)
             treeview.insert('', position, identifier, text = file_name)
             treeview.set(identifier, 'File Path', file_path)
         else:
             malware_name = str(line)
             treeview.set(identifier, 'Malware', malware_name)
             #treeview.insert(identifier, 'end', 'Malware', text = malware_name)
         current_file = file_name
         item_count = item_count + 1
         line_count = line_count + 1
         count = count + 1
    file.close()

    treeview.config(height = 20)
    treeview.place(relx = 0.01, rely = 0.02)


def logs():
    window3 = Toplevel(window, highlightcolor = '#4a3cc4', highlightbackground = '#4a3cc4', highlightthickness = 0.5)
    window3.geometry("1050x470")
    window3.configure(background  = 'black')
    window3.title('Logs')
    treeview2 = ttk.Treeview(window3)
    style = ttk.Style(window3)
    # set ttk theme to "clam" which support the fieldbackground option
    style.theme_use("clam")
    style.configure("Treeview", background="#4a3cc4", fieldbackground="#4a3cc4", foreground="white")


    treeview2.column('#0', width = 620)
    treeview2.heading('#0', text = 'Path')
    treeview2.config(columns = ('Malware_ID', 'Date_ID', 'Time_ID', 'scan_type_ID'))
    treeview2.heading('Malware_ID', text = 'Malware')
    treeview2.heading('Date_ID', text = 'Date')
    treeview2.heading('Time_ID', text = 'Time')
    treeview2.heading('scan_type_ID', text = 'Scan Type')
    treeview2.column('Malware_ID', width = 100)
    treeview2.column('Date_ID', width = 100)
    treeview2.column('Time_ID', width = 100)
    treeview2.column('scan_type_ID', width = 100)



    db = database.initialise_db('root', 'Narnia0102*')
    query = "SELECT * FROM scan_completed"
    response = database.query_select(query, db)
    print response
    print len(response)


    if(response != []):
        for x in range(len(response)):
            identifier = 'item' + str(x)

            for x1 in range(0, 5):

                if(x1 == 0):
                    treeview2.insert('', x, identifier, text = response[x][x1])
                if(x1 == 1):
                    treeview2.set(identifier, 'Malware_ID', response[x][x1])
                if(x1 == 2):
                    treeview2.set(identifier, 'Date_ID', response[x][x1])

                if(x1 == 3):
                    treeview2.set(identifier, 'Time_ID', response[x][x1])

                if(x1 == 4):
                     print "scan type is: ", response[x][x1]
                     treeview2.set(identifier, 'scan_type_ID', response[x][x1])


    treeview2.config(height = 20)
    treeview2.place(relx = 0.01, rely = 0.02)




def create_window():

    global file_path
    print file_path
    global window2
    progressBar2.destroy()
    initialise_setup.destroy()
    #window2 = Toplevel(window, highlightcolor = 'white', highlightbackground = 'white', highlightthickness = 0.5)
    window2.geometry("400x250")
    window2.configure(background = 'black')
    window2.title('Choose File or Directory to Scan')



    global open_dir_bt
    open_dir_bt = Button(window2)
    image_1 = PhotoImage(file = 'Directory.png')
    label = Label(image = image_1)
    label.image = image_1
    open_dir_bt.config(image = image_1, background = 'black',activebackground = '#5894f4', borderwidth = 0, highlightthickness = 0)
    open_dir_bt.bind('<Button-1>', open_directory_browser )
    open_dir_bt.place(relx =0.20, rely =0.25)

    global open_dir_label
    open_dir_label = Label(window2, text = 'Scan Directory')
    open_dir_label.configure(background = 'black', fg = 'white')
    open_dir_label.place(relx = 0.32, rely = 0.70, anchor = 'center')

    global open_file_bt
    open_file_bt = Button(window2)
    image_2 = PhotoImage(file = 'single_file.png')
    label2 = Label(image = image_2)
    label2.image = image_2
    open_file_bt.config(image = image_2, background = 'black',activebackground = '#5894f4', borderwidth = 0, highlightthickness = 0)
    open_file_bt.bind('<Button-1>', open_file_browser )
    open_file_bt.place(relx =0.55, rely =0.25)

    global open_file_label
    open_file_label = Label(window2, text = 'Scan File')
    open_file_label.configure(background = 'black', fg = 'white')
    open_file_label.place(relx = 0.68, rely = 0.70, anchor = 'center')

    global next_arrow
    next_arrow = Button(window2)
    image_3 = PhotoImage(file = 'arrow.png')
    label3 = Label(image = image_3)
    label3.image = image_3
    next_arrow.config(image = image_3, background = 'black', command = scan_type_window, borderwidth = 0, highlightthickness = 0)
    next_arrow.place(relx =0.85, rely =0.75)




def inc_progress_bar(percentage_complete):
    global progress_bar
    #This value will come from the number of bytes scanned at the moment the progress bar is called.
    progressBar['value'] = percentage_complete
    progressBar.update()

def create_scan_finished_button():
    global found_malware
    global window2
    global pause_button
    global resume_button
    global next
    pause_button.destroy()
    resume_button.destroy()

    #If the user is an advanced user go to the action page otherwise delete the signatures for the user.
    #obtain the type of user

    db = database.initialise_db('root', 'Narnia0102*')
    query = 'SELECT user_type FROM user_info WHERE user_name = "' + username.get() + '";'
    response = database.query_select(query, db)
    global user_type
    user_type = response[0][0]

    #scanning mode 1 is the


    if(scanning_mode == 1):
        if(str(user_type) == 'advanced'):
            response = found_malware['text']
            #if there any infected files have been found
            if(response != 0):
                next = Button(window2, text = 'Next', width = 10, command = action_page)
                next.configure(background = 'black', fg = 'white')
                next.bind('<button-1>')
                next.place(relx = 0.44, rely = 0.87)
            else:
                close = Button(window2, text = 'Close', width = 10, command = window2.destroy)
                close.configure(background = '#00cc44', fg = 'white')
                close.bind('<button-1>')
                close.place(relx = 0.46, rely = 0.87)
        elif(str(user_type) == 'simple'):
            response = found_malware['text']
            #if there any infected files have been found
            if(response != 0):
                next = Button(window2, text = 'Next', width = 10, command = delete_malare_simple_user)
                next.configure(background = 'black', fg = 'white')
                next.bind('<button-1>')
                next.place(relx = 0.44, rely = 0.87)
            else:
                close = Button(window2, text = 'Close', width = 10, command = window2.destroy)
                close.configure(background = '#00cc44', fg = 'white')
                close.bind('<button-1>')
                close.place(relx = 0.46, rely = 0.87)


    if(scanning_mode == 0):
        response = changed_files['text']

        # db = database.initialise_db('root', 'Narnia0102*')
        # query = 'SELECT user_type FROM user_info WHERE user_name = "' + username.get() + '";'
        # response = database.query_select(query, db)
        # print response

        if(response != 0):
            next = Button(window2, text = 'Next', width = 10, command = integrity_scan_results_page)
            next.configure(background = 'black', fg = 'white')
            next.bind('<button-1>')
            next.place(relx = 0.44, rely = 0.87)
        else:
            close = Button(window2, text = 'Close', width = 10, command = window2.destroy)
            close.configure(background = '#00cc44', fg = 'white')
            close.bind('<button-1>')
            close.place(relx = 0.46, rely = 0.87)
    # #if(user_type.get() == 'simple'):
    #     if(response != 0):
    #         next = Button(window2, text = 'Next', width = 10, command = malware_deleted_page)
    #         next.configure(background = 'black', fg = 'white')
    #         next.bind('<button-1>')
    #         next.place(relx = 0.44, rely = 0.87)
    #     else:
    #         close = Button(window2, text = 'Close', width = 10, command = window2.destroy)
    #         close.configure(background = '#00cc44', fg = 'white')
    #         close.bind('<button-1>')
    #         close.place(relx = 0.46, rely = 0.87)




def initialisation_window():
    global progressBar2
    global window2
    global initialise_setup
    window2 = Toplevel(window, highlightcolor = '#4a3cc4', highlightbackground = '#4a3cc4', highlightthickness = 0.5)
    window2.geometry("835x250")
    window2.configure(background  = 'black')
    s = ttk.Style()
    s.theme_use('clam')
    s.configure("#4a3cc4.Horizontal.TProgressbar", foreground='#4a3cc4', background='#4a3cc4')
    progressBar2 = ttk.Progressbar(window2, style="#4a3cc4.Horizontal.TProgressbar", orient = HORIZONTAL, length = 750)
    progressBar2.config(mode = 'determinate')
    progressBar2.place(relx = 0.05, rely = 0.40)
    progressBar2['value'] = 0
    progressBar2['maximum'] = 100
    progressBar2.update()
    print "initialise scanning"
    initialise_setup = Label(window2, text = "Initialising, may take a few minutes...")
    initialise_setup.configure(background = 'black', fg = 'white', font = ('Helvetica', 15))
    initialise_setup.place(relx = 0.30, rely = 0.20)
    initialise_setup.update()
    global times_initialised
    if(times_initialised == 0):
        initialise_scanning()
    create_window()

def scan_type_window():
    global  window2
    open_file.destroy()
    # window2 = Toplevel(window)
    # window2.geometry("800x300")
    # window2.configure(background = 'grey')
    # window2.title('Choose File or Directory to Scan')
    global integrity_check_bt
    global virus_scan_bt
    integrity_check_bt = Button(window2, text = 'Check file/directory \n for changes', command = integrity_checking,  height = 10, width = 20, background = 'dark grey')
    integrity_check_bt.bind('<Button-1>')
    integrity_check_bt.place(relx = 0.22, rely = 0.20)

    virus_scan_bt = Button(window2, text = 'Virus Scan', height = 10, width = 20, background = 'dark grey', command = virus_scan_window)
    virus_scan_bt.bind('<Button-1>')
    virus_scan_bt.place(relx = 0.55, rely = 0.20)



def callback(event):
    #returns a dictionary containing the values in the selected row.
    global current_item_identifier
    current_item_identifier  = treeview.selection()
    Dictionary = treeview.item(current_item_identifier)
    values_ret = Dictionary.get('values')
    global filePath
    filePath = values_ret[0]


def action_page():
    global window2
    window2.configure(background = "Black")
    window2.title('Results')
    progressBar.destroy()
    pause_button.destroy()
    resume_button.destroy()
    percentage_complete_label.destroy()
    found_malware.destroy()
    scanned_files.destroy()
    found_malware.destroy()
    found.destroy()
    current_files_scanning.destroy()
    number_of_files_scanned.destroy()
    scanning.destroy()
    next.destroy()
    #
    # scroller = Scrollbar(window2, command=output.yview)
    # scroller.place(relx = 0.475, rely = 0.65)

    # output['yscrollcommand'] = scroller.set
    #
    # output.insert(END, "Scan Results:")
#---
    # global listbox
    # listbox = Listbox(window2, width = 65, height = 20)
    # listbox.bind('<ButtonRelease-1>', Select_from_listbox)
    # listbox.place(relx = 0.30, rely = 0.20)
    #
    # # listbox.xscrollbar.pack(side=BOTTOM, fill=X)
    # # listbox.yscrollbar.pack(side=BOTTOM, fill=Y)
    #
    # file = open("infected_files.txt")
    # for line in file:
    #      print line
    #      listbox.insert(END, line)
    # file.close()


#---
    global window2
    window2.configure(background = "Black")
    create_malware_results_treeview()
    delete_virus1 = Button(window2, text = 'Delete virus', command = delete_virus)
    delete_virus1.bind("<Button-1>")
    delete_virus1.place(relx = 0.01, rely = 0.85)

    quarantine = Button(window2, text = 'Quarantine', command = quarantine_file)
    quarantine.configure(background = '#00cc44')
    quarantine.bind("<Button-1>")
    quarantine.place(relx = 0.14, rely = 0.85)

def quarantine():
    window4 = Toplevel(window, highlightcolor = '#4a3cc4', highlightbackground = '#4a3cc4', highlightthickness = 0.5)
    window4.geometry("1000x470")
    window4.configure(background  = 'black')
    window4.title('Quarantine Logs')
    treeview4 = ttk.Treeview(window4)
    style = ttk.Style(window4)
# set ttk theme to "clam" which support the fieldbackground option
    style.theme_use("clam")
    style.configure("Treeview", background="#4a3cc4", fieldbackground="#4a3cc4", foreground="white")
    treeview4.column('#0', width = 370)
    treeview4.heading('#0', text = 'Infected File')
    treeview4.config(columns = ('Malware_ID', 'Action Taken_ID'))
    treeview4.heading('Malware_ID', text = 'Malware')
    treeview4.heading('Action Taken_ID', text = 'Action Taken')
    treeview4.column('Malware_ID', width = 400)
    treeview4.bind('<<TreeviewSelect>>', callback)
    treeview4.config(height = 20)
    treeview4.place(relx = 0.01, rely = 0.02)



def create_configuration_window():


    global config_window
    config_window = Toplevel(window, highlightcolor = '#4a3cc4', highlightbackground = '#4a3cc4', highlightthickness = 0.5)
    config_window.title("Configuration")
    config_window.geometry("800x500")
    config_window.configure(background = "black")
    #==== Configuration page



    deep_scan = BooleanVar()
    medium_scan = BooleanVar()
    shallow_scan = BooleanVar()
    email_results = BooleanVar()
    frequency = StringVar()

    config_label = Label(config_window, text = 'Configuration')
    config_label.config(background = 'Grey', font =('Courier', 30), fg = 'black')
    config_label.place(relx = 0.01, rely = 0.01)

    day_choice = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Everyday'}
    day = StringVar(config_window)
    #default
    day.set('Everyday')
    scheduledDay = OptionMenu(config_window, day, *day_choice)
    scheduledDay.place(relx = 0.01, rely = 0.20)

    time_choice = ('')
    time = StringVar()
    time.set('00:00')
    scheduledTime = OptionMenu(config_window, time, time_choice)
    scheduledTime.place(relx = 0.16, rely = 0.20)

    frequency_choice = {'Every week', 'Every fortnight'}
    frequency.set('Every Week')
    scheduledFrequency = OptionMenu(config_window, frequency, *frequency_choice)
    scheduledFrequency.place(relx = 0.31, rely = 0.20)

    scanType = Label(config_window, text = 'Scan Type: The scan type is relating to the quality of scan, time: deep > medium > shallow')
    scanType.configure(background = 'Grey', fg = 'blue')
    scanType.place(relx = 0.01, rely = 0.31)

    checkbutton_scanType_deep = Checkbutton(config_window, text = "Deep", variable = deep_scan)
    checkbutton_scanType_deep.configure(background = 'Grey', fg = 'black')
    checkbutton_scanType_deep.place(relx= 0.01, rely= 0.36)


    checkbutton_scanType_medium = Checkbutton(config_window, text = 'medium', variable = medium_scan)
    checkbutton_scanType_medium.configure(background = 'Grey', fg = 'black')
    checkbutton_scanType_medium.place(relx= 0.16, rely= 0.36)


    checkbutton_scanType_shallow = Checkbutton(config_window, text = 'shallow', variable = shallow_scan)
    checkbutton_scanType_shallow.configure(background = 'Grey', fg = 'black')
    checkbutton_scanType_shallow.place(relx= 0.31, rely = 0.36)


    checkbutton_email = Checkbutton(config_window, text = 'Email scan results', variable = email_results)
    checkbutton_email.place(relx = 0.01, rely = 0.46)
    #checkbutton_email.configure(background = 'black', fg = 'white')


    manual_update = Button(config_window, text = 'Manual Update', command = update_datatbase)
    manual_update.bind('<Button-1>')
    manual_update.configure(background = 'white', fg = 'black')
    manual_update.place(relx = 0.01, rely = 0.61)

    last_update = '21-01-2019'
    global date_update
    date_update = Label(config_window, text = last_update)
    date_update.configure(background = 'white', fg = 'red')
    date_update.place(relx = 0.13, rely = 0.56)
    virus_database_update_label = Label(config_window, text = 'Last Updated: ' )
    virus_database_update_label.configure(background = 'white', fg = 'blue')
    virus_database_update_label.place(relx = 0.01, rely = 0.56)

    #need to place and create variables for the checkbuttons.S

    or_label = Label(config_window, text = 'or')
    or_label.configure(background = 'white', fg = 'black')
    or_label.place(relx = 0.20, rely = 0.61)

    checkbutton_automatic_db_update = Checkbutton(config_window, text = 'Automatic Update')
    checkbutton_automatic_db_update.configure(background = 'white', fg = 'black')
    checkbutton_automatic_db_update.place(relx = 0.26, rely = 0.61)
    global simple_user
    simple_user = BooleanVar()
    global advanced_user
    advanced_user = BooleanVar()

    simple_user_CB = Checkbutton(config_window, text = 'Simple User', variable=simple_user, command = user_fn)
    #simple_user_CB.configure(background = 'black', fg = 'white')
    simple_user_CB.place(relx = 0.01, rely = 0.70)

    advanced_user_CB = Checkbutton(config_window, text = 'Advanced User', variable=advanced_user, command = user_fn)
    #advanced_user_CB.configure(background = 'black', fg = 'white')
    advanced_user_CB.place(relx = 0.15, rely = 0.70)

    db = database.initialise_db('root', 'Narnia0102*')
    query = 'SELECT user_type FROM user_info WHERE user_name = "' + username.get() + '";'
    response = database.query_select(query, db)
    print 'The user type is: ', response[0][0]

    #===

#TODO create a function (too much repetative code)
window = Tk()
window.geometry("1100x700")
window.title("Aware Antivirus")




f3 = Frame(window)
f3.configure(background = "Black")
f3.grid_propagate(0)

f1 = Frame(window, width = 1100, height = 700)
f1.configure(background = "Black")
f1.grid_propagate(0)

f2 = Frame(window)
f2.configure(background = "Black")
f2.grid_propagate(0)

f4 = Frame(window)
f4.configure(background = "Black")
f4.grid_propagate(0)

f5 = Frame(window)
f5.configure(background = "Black")
f5.grid_propagate(0)

f6 = Frame(window, highlightcolor = '#4a3cc4', highlightbackground = '#4a3cc4')
f6.configure(background = "Black")
f6.grid_propagate(0)

f7 = Frame(window)
f7.configure(background = "Black")
f7.grid_propagate(0)

logs_pg = Frame(window)
logs_pg.configure(background = "Black")
logs_pg.propagate(0)

config_window = Toplevel(window)
window.configure(background = "Black")
date_update = Label(config_window, text = '')

for frame in (f1, f2, f3, f4, f5, f6, f7, logs_pg):
    frame.grid(row = 1000, column = 1000, sticky = 'news')

logo3 = PhotoImage(file="Aware_logo3+.png")
logo3_label = Label(f3, image=logo3)
logo3_label.configure(background = 'black')
logo3_label.image  = logo3
logo3_label.place(relx=0.43, rely=0.4, anchor=CENTER)

logo4 = PhotoImage(file="antivirus_logo.png")
logo4_label = Label(f3, image=logo4)
logo4_label.configure(background = 'black')
logo4_label.image  = logo4
logo4_label.place(relx=0.43, rely=0.575, anchor=CENTER)

logo5 = PhotoImage(file="Aware_logo3+.png")
logo5_label = Label(f4, image=logo5)
logo5_label.configure(background = 'black')
logo5_label.image  = logo5
logo5_label.place(relx=0.50, rely=0.20, anchor=CENTER)

logo6 = PhotoImage(file="antivirus_logo.png")
logo6_label = Label(f4, image=logo6)
logo6_label.configure(background = 'black')
logo6_label.image  = logo6
logo6_label.place(relx=0.50, rely=0.34, anchor=CENTER)

login_label = Label(f1, text = "Login:")
login_label.grid(row = 0, column = 0)
login_label.configure(background = "Black", fg = "White")

register_label = Label(f2, text = "   Register:")
register_label.grid(row =1, column = 10)
register_label.configure(background = "Black", fg = "White")

select_login = Button(f3, text = 'Login', command= lambda:raise_frame(f1))
select_login.place(relx=0.35, rely = 0.64)

select_register = Button(f3, text = 'Register', command= lambda:raise_frame(f2))
select_register.place(relx=0.43, rely = 0.64)

#global variables
value = StringVar()
variable = StringVar()
username = StringVar()
password = StringVar()
new_username = StringVar()
new_password = StringVar()
re_new_password = StringVar()
show_pass = BooleanVar()
username1 = StringVar()
file_path = StringVar()
Date = StringVar
window2 = ""
next = ""
open_file = ""
progressBar = ""
counter = 0
integrity_check_bt = ''
virus_scan_bt = ''
current_files_scanning = ''
results = ''
percentage_complete_label = ''
number_of_files_scanned = ''
found_malware = ''
pause_button = ''
resume_button = ''
scanned_files = ''
scanning = ''
found = ''
listbox = ''
treeview = ''
filePath = ''
current_item_identifier = ''
times_initialised = 0
number_of_viruses_found = 0
percentage_complete = 0
total = 0
number_of_files = 0
number_of_files_scanned_today = 0
background_image = ''
open_file_bt = ''
open_file_label = ''
open_dir_bt = ''
open_file_label = ''
next_arrow = ''
progressBar2 = ''
initialise_setup = ''
changed_files = ''
scanning_mode = ''
number_of_changed_files = ''
simple_user = ''
advanced_user = ''
user_type = ''


# def virus_scan_page()


def virus_scan_window():
    open_file_bt.destroy()
    open_file_label.destroy()
    open_dir_bt.destroy()
    open_dir_label.destroy()
    next_arrow.destroy()
    integrity_check_bt.destroy()
    virus_scan_bt.destroy()
    global window2
    global scanning
    global scanned_files
    window2.geometry("920x530")
    window2.configure(background = "black")
    global scanning_mode
    scanning_mode = 1

    scanning = Label(window2, text = 'Scanning file: ')
    scanning.configure(background = 'black', fg = 'white')
    scanning.place(relx = 0.02, rely = 0.10)
    global current_files_scanning

    global progressBar
    s = ttk.Style()
    s.theme_use('clam')
    s.configure("#4a3cc4.Horizontal.TProgressbar", foreground='#4a3cc4', background='#4a3cc4')
    progressBar = ttk.Progressbar(window2, style="#4a3cc4.Horizontal.TProgressbar", orient = HORIZONTAL, length = 890)
    progressBar.config(mode = 'determinate')
    progressBar.place(relx = 0.02, rely = 0.70)

    current_files_scanning = Label(window2, text = '', borderwidth=2)
    current_files_scanning.configure(background = 'black')
    current_files_scanning.place(relx = 0.15, rely = 0.10)
    global number_of_files_scanned
    number_of_files_scanned = Label(window2, text = '', borderwidth=2, relief = 'groove')
    number_of_files_scanned.configure(background ='#4a3cc4', fg = 'white', font = ('Helvetica', 30, 'bold'), width = 10)
    number_of_files_scanned.place(relx = 0.24, rely = 0.40)

    scanned_files = Label(window2, text='Scanned')
    scanned_files.configure(background = 'black', fg = 'white')
    scanned_files.place(relx = '0.33', rely = '0.50')

    global found_malware
    found_malware = Label(window2, text = '', borderwidth = 2, relief = 'groove')
    found_malware.configure(background = '#4a3cc4', fg = 'white', font = ('Helvetica', 30, 'bold'), width = 10)
    found_malware.place(relx = '0.52', rely = '0.40')
    global found
    found = Label(window2, text='Found')
    found.configure(background = 'black', fg = 'white')
    found.place(relx = '0.62', rely = '0.50')

    global percentage_complete_label
    percentage_complete_label = Label(window2, text = '')
    percentage_complete_label.configure(background = 'black', fg = 'white')
    percentage_complete_label.place(relx = 0.02, rely = 0.65)

    global pause_button
    pause_button = Button(window2, text = 'Pause', width = 10)
    pause_button.bind('<button-1>')
    pause_button.configure(background = 'black', fg = 'white', font = ('Helvetica', 12, 'bold'))
    pause_button.place(relx = 0.37, rely = 0.87)

    global resume_button
    resume_button = Button(window2, text = 'Resume', width = 10)
    resume_button.bind('<button-1>')
    resume_button.configure(background = 'black', fg = 'white', font = ('Helvetica', 12, 'bold'))
    resume_button.place(relx = 0.52, rely = 0.87)

    progressBar['value'] = 0
    #This value will come from the number of bytes of the file or directory.
    progressBar['maximum'] = 100

    #perform the scan
    scan()






def get_test():
    un = username.get()
    username22 = Button(f6, text = un)
    username22.bind('<button-1>')
    username22.configure(background = 'black', fg = 'light blue')
    username22.place(relx = 0.10, rely =0.01 )

reg_username_label = Label(f2, text = "   Username: ")
reg_username_label.configure(background = "Black", fg = "white")
reg_username_label.grid(row = 5, column = 10)
reg_username_entry_path = Entry(f2, textvariable=new_username)
reg_username_entry_path.grid(row = 5, column = 11)

reg_password_entry_path = Entry(f2,  show = "*", textvariable = new_password)
reg_password_entry_path.grid(row = 6, column = 11)
reg_password_label = Label(f2, text = "   Password: ")
reg_password_label.configure(background = "Black", fg = "white")
reg_password_label.grid(row = 6, column = 10)
#reg_secretword_entry_path

re_reg_password_entry_path = Entry(f2,  show = "*", textvariable = re_new_password)
re_reg_password_entry_path.grid(row = 7, column = 11)
re_reg_password_label = Label(f2, text = "   Re-enter: ")
re_reg_password_label.configure(background = "Black", fg = "white")
re_reg_password_label.grid(row = 7, column = 10)

register_button = Button(f2, text = 'register')
register_button.bind("<Button-1>", register_new_user)
register_button.grid(row = 9, column = 11)

show_password1 = Checkbutton(f2, text="show password", variable = show_pass, command = show_password)
show_password1.configure(background = "Black", fg = "white")
show_password1.grid(row = 8, column = 10)

back_to_main_page_button_reg = Button(f2, text='Go back', command= lambda:raise_frame(f3))
back_to_main_page_button_reg.grid(row = 0, column = 0)

back_to_main_page_button_reg = Button(f1, text='Go back', command= lambda:raise_frame(f3))
back_to_main_page_button_reg.grid(row = 8, column = 1)

output = Text(f4, width = 70, height = 40)
output.place(relx = 0.0010, rely = 0.47)

scroller = Scrollbar(f4, command=output.yview)
scroller.place(relx = 0.475, rely = 0.65)

output['yscrollcommand'] = scroller.set
output.insert(END, "Scan Results:")


open_file = Button(f4, text = 'open file')
open_file.bind("<Button-1>", open_file_browser)
open_file.place(relx = 0.001, rely = 0.42)
#dropdown = OptionMenu(f4, variable, "file1", "file2", "file3")
#dropdown.configure(background = "Black")
#dropdown.grid(column = 60, ro_w = 3)

#causes transition to a page which shows the types of scans available
run = Button(f4, text = 'Run Virus Scan', command = virus_scan_window)
run.bind("<Button-1>")
run.place(relx = 0.08, rely = 0.42)


logged_in_as_label = Label(f4, text = 'logged in as: ');
logged_in_as_label.place(relx = 0.63, rely = 0.01 )

configuration_button = Button(f4, text = 'Configuration', command = create_configuration_window)
configuration_button.bind('<Button-1>')
configuration_button.configure(font =('Courier'))
configuration_button.place(relx = 0.01 , rely = 0.01)

def return_1():
    return 1
option = 0
logo5 = PhotoImage(file="Aware_logo3+.png")
logo5_label = Label(f7, image=logo5)
logo5_label.configure(background = 'black')
logo5_label.image  = logo5
logo5_label.place(relx=0.50, rely=0.10, anchor=CENTER)

logo6 = PhotoImage(file="antivirus_logo.png")
logo6_label = Label(f7, image=logo6)
logo6_label.configure(background = 'black')
logo6_label.image  = logo6
logo6_label.place(relx=0.50, rely=0.23, anchor=CENTER)

username_label = Label(f7, text = "Username: ")
username_label.configure(background = "Black", fg = "white")
username_label.place(relx = 0.34 ,  rely = 0.47)

username_entry_path = Entry(f7, textvariable = username)
username_entry_path.place(relx = 0.34, rely = 0.50)

password_label = Label(f7, text = "Password: ")
password_label.configure(background = "Black", fg = "white")
password_label.place(relx = 0.50, rely = 0.47)

password_entry_path = Entry(f7, textvariable = password)
password_entry_path.place(relx = 0.50, rely = 0.50)

submit_button = Button(f7, text = 'Submit')
submit_button.bind("<Button-1>", save_login_details)
submit_button.place(relx = 0.55, rely = 0.55)

#=====: Front option page

logo = PhotoImage(file = 'AAV2_logo.png')
logo_label = Label(f6, image = logo)
logo_label.configure(background = 'black')
logo_label.image = logo
logo_label.place(relx = 0.52, rely = 0.087, anchor = 'center')

quarantine_button = Button(f6)
photo = PhotoImage(file = 'quarantine.png')
quarantine_button.config(image = photo, background = 'black',activebackground = '#5894f4', command = quarantine, borderwidth = 0, highlightthickness = 0)
quarantine_button.place(relx = 0.33, rely = 0.72)

quarantine_label = Label(f6, text = 'Quarantine Logs')
quarantine_label.configure(background = 'black', fg = 'light blue')
quarantine_label.place(relx = 0.33, rely = 0.90)

file_scan_button = Button(f6)
photo2 = PhotoImage(file =  'scan.png')
file_scan_button.config(image = photo2, background = 'black',activebackground = '#5894f4', command = initialisation_window, borderwidth = 0, highlightthickness = 0)
file_scan_button.place(relx = 0.56, rely = 0.72)

file_scan_label = Label(f6, text = 'Scan Files')
file_scan_label.configure(background = 'black', fg = 'light blue')
file_scan_label.place(relx = 0.585, rely = 0.90)

settings_button = Button(f6)
photo3 = PhotoImage(file = 'settings_logo2.png')
settings_button.config(image = photo3, background = 'black',activebackground = '#5894f4', command = create_configuration_window , borderwidth = 0, highlightthickness = 0)
settings_button.place(relx = 0.78, rely = 0.72)

settings_label = Label(f6, text = 'Settings')
settings_label.configure(background = 'Black', fg = 'light Blue')
settings_label.bind('<Button-1>')
settings_label.place(relx = 0.81, rely = 0.90)

logs_button = Button(f6)
photo4 = PhotoImage(file = 'logs.png')
logs_button.config(image = photo4, background = 'black',activebackground = 'black', command = logs , borderwidth = 0, highlightthickness = 0)
logs_button.bind('<Button-1>')
logs_button.place(relx = 0.10, rely = 0.72)

logs_label = Label(f6, text = 'logs')
logs_label.configure(background = 'Black', fg = 'light Blue')
logs_label.place(relx = 0.135, rely = 0.90)

logged_in_as = Label(f6, text = 'logged in as: ')
logged_in_as.configure(background = 'black', fg = 'white')
logged_in_as.place(relx = 0.01, rely = 0.01)

files_scanned_today = Label(f6, text = 'Files scanned today')
files_scanned_today.configure(background = 'black', fg = 'white')
files_scanned_today.place(relx = 0.495, rely=0.50, anchor = 'center')

number_scanned = get_number_of_files_scanned()
global number_of_files_scanned_today
number_of_files_scanned_today = Label(f6, text = number_scanned)
number_of_files_scanned_today.configure(background = 'black', fg = 'white', font = ('Helvetica', 40))
number_of_files_scanned_today.place(relx = 0.495, rely = 0.43, anchor = 'center')

greeting = Label(f6, text = 'Ahoy, Nadia')
greeting. configure(background = 'black', fg = 'white', font = ('Helvetica', 20))
greeting.place(relx = 0.495, rely = 0.35, anchor = 'center')

#TODO merge integrity_checking and virus_scan -  think about it
def integrity_checking():

    open_file_bt.destroy()
    open_file_label.destroy()
    open_dir_bt.destroy()
    open_dir_label.destroy()
    next_arrow.destroy()
    integrity_check_bt.destroy()
    virus_scan_bt.destroy()
    global window2
    global scanning
    global scanned_files
    window2.geometry("920x530")
    window2.configure(background = "black")
    global scanning_mode
    scanning_mode = 0

    scanning = Label(window2, text = 'Scanning file: ')
    scanning.configure(background = 'black', fg = 'white')
    scanning.place(relx = 0.02, rely = 0.10)
    global current_files_scanning

    global progressBar
    s = ttk.Style()
    s.theme_use('clam')
    s.configure("#4a3cc4.Horizontal.TProgressbar", foreground='#4a3cc4', background='#4a3cc4')
    progressBar = ttk.Progressbar(window2, style="#4a3cc4.Horizontal.TProgressbar", orient = HORIZONTAL, length = 890)
    progressBar.config(mode = 'determinate')
    progressBar.place(relx = 0.02, rely = 0.70)

    current_files_scanning = Label(window2, text = '', borderwidth=2)
    current_files_scanning.configure(background = 'black')
    current_files_scanning.place(relx = 0.15, rely = 0.10)

    global number_of_files_scanned
    number_of_files_scanned = Label(window2, text = '', borderwidth=2, relief = 'groove')
    number_of_files_scanned.configure(background ='#4a3cc4', fg = 'white', font = ('Helvetica', 30, 'bold'), width = 10)
    number_of_files_scanned.place(relx = 0.24, rely = 0.40)

    scanned_files = Label(window2, text='Scanned')
    scanned_files.configure(background = 'black', fg = 'white')
    scanned_files.place(relx = '0.33', rely = '0.50')

    global changed_files
    changed_files = Label(window2, text = '', borderwidth = 2, relief = 'groove')
    changed_files.configure(background = '#4a3cc4', fg = 'white', font = ('Helvetica', 30, 'bold'), width = 10)
    changed_files.place(relx = '0.52', rely = '0.40')

    global found
    found = Label(window2, text='File Changed')
    found.configure(background = 'black', fg = 'white')
    found.place(relx = '0.62', rely = '0.50')

    global percentage_complete_label
    percentage_complete_label = Label(window2, text = '')
    percentage_complete_label.configure(background = 'black', fg = 'white')
    percentage_complete_label.place(relx = 0.02, rely = 0.65)

    global pause_button
    pause_button = Button(window2, text = 'Pause', width = 10)
    pause_button.bind('<button-1>')
    pause_button.configure(background = 'black', fg = 'white', font = ('Helvetica', 12, 'bold'))
    pause_button.place(relx = 0.37, rely = 0.87)

    global resume_button
    resume_button = Button(window2, text = 'Resume', width = 10)
    resume_button.bind('<button-1>')
    resume_button.configure(background = 'black', fg = 'white', font = ('Helvetica', 12, 'bold'))
    resume_button.place(relx = 0.52, rely = 0.87)

    progressBar['value'] = 0
    #This value will come from the number of bytes of the file or directory.
    progressBar['maximum'] = 100
    scan()

def integrity_scan_results_page():
    global window2
    window2.geometry("700x460")
    window2.title("Integrity Scan Results")
    progressBar.destroy()
    number_of_files_scanned.destroy()
    pause_button.destroy()
    resume_button.destroy()
    changed_files.destroy()
    percentage_complete_label.destroy()
    found.destroy()
    next.destroy()
    current_files_scanning.destroy()
    position = 0
    str_position = str(position)
    identifier = 'item' + str(position)
    treeview = ttk.Treeview(window2)
    style = ttk.Style(window2)
    # set ttk theme to "clam" which support the fieldbackground option
    style.theme_use("clam")
    style.configure("Treeview", background="#4a3cc4", fieldbackground="#4a3cc4", foreground="white")
    treeview.column('#0', width = 680)
    treeview.heading('#0', text = 'Change file/s')
    #printing the changed files to the treeview
    file = open("changed_files.txt", "r")
    for line in file:
        treeview.insert('', str_position, identifier, text = line)
        position = position + 1
        str_position = str(position)
        identifier = 'item' + str(position)
    file.close()

    treeview.config(height = 20)
    treeview.place(relx = 0.01, rely = 0.02)



raise_frame(f7)
window.mainloop()
