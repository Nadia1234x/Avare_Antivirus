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

def quarantine_file():
    output = pyaes.AESModeOfOperationCBC(key)
    
def delete_virus():
    print "filename: ", value
    file_name = value
    print file_name
    Aho_Corasick.main(file_name, "delete")

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

#TODO calculate the total bytes of the files to be scanned, then as each file is scanned, obtain the number of bytes of that file and calculate the percentage.

def initialise_scanning():
    print "initialising..."
    file_integrity_check.initialise()


def iterate_files():
        percentage_complete = 0
        total_files_size = calculate_file_bytes()
        total = 0
        number_of_files = 0
        number_of_viruses_found = 0
        for root, dirs, files in os.walk('/home/nadia/Desktop/Third_Year_Project/virus_checker_test', topdown=False):
            for file in files:
                file = os.path.join(root, file)
                response = file_integrity_check.main(file, 'Nadia23')
                number_of_viruses_found = number_of_viruses_found + response
                global found_malware
                found_malware['text'] = number_of_viruses_found
                    #number_of_viruses_found
                found_malware.update()


                current_file_size = os.path.getsize(file)
                total = total + current_file_size
                number_of_files = number_of_files + 1
                percentage_complete = percentage_complete + ((Decimal(current_file_size)/Decimal(total_files_size)) * 100)
                print str(percentage_complete) + ' %'

                global percentage_complete_label
                percentage_complete_label['text'] = str(percentage_complete) + '% complete'

                #increase the progress bar depending on how many bytes of files have been scanned.
                inc_progress_bar(percentage_complete)

                current_files_scanning['fg'] = 'white'
                current_files_scanning['text'] = str(file)
                global number_of_files_scanned
                number_of_files_scanned['text'] = str(number_of_files)
                number_of_files_scanned.update()


                time.sleep(0.0001)
                current_files_scanning.update()
                # count = count + 1
                # if(count == 10):
                #     sys.exit()
        #TODO change this later so that the final number rounds to 100
        current_files_scanning['text'] = 'Scan complete'
        create_scan_finished_button()


def calculate_file_bytes():
      total = 0
      for root, dirs, files in os.walk('/home/nadia/Desktop/Third_Year_Project/virus_checker_test', topdown=False):
            for file in files:
                file = os.path.join(root, file)
                total = total + os.path.getsize(file)
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
    global username1
    username1 = username.get()
    password1 = password.get()
    response = check_login_details.validate_credentials(str(username1), str(password1))
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


def open_program():
    create_window()
    time.sleep(10)
    global count
    count = count + 1
    output.insert(END, "\n Scan in progress please wait... \n")
    output.update_idletasks()
    time.sleep(2)

    print type(file_path)
    print "file path: ", file_path
    if(count == 1):
        file_integrity_check.initialise()

    #may want to put some of this in a new method
    file_integrity_check.main(file_path, "Nadia23")
    output.insert(END, "Scan finished \n")
    output.insert(END, "Found: \n")
    file = open("results_file.txt", "r")
    for line in file:
        output.insert(END, line)
    file.close()

    # file = open("infected_files.txt")
    # for line in file:
    #      listbox.insert(END, line)
    # file.close()

    #if infected files are found give option to delete of quarantine the files.
    any_files_infected = os.stat("infected_files.txt").st_size == 0
    if(any_files_infected == False):
        quarantine = Button(f4, text = 'quarantine', command = create_window())
        quarantine.place(relx = 0.62, rely = 0.42)


def create_window():

    global file_path
    print file_path

    global window2
    window2 = Toplevel(window)
    window2.geometry("920x530")
    window2.configure(background = 'grey')
    window2.title('Choose File or Directory to Scan')
    # open_file = Button(window2, text = 'open file')
    # open_file.bind("<Button-1>", open_file_browser)
    # open_file.place(relx = 0.001, rely = 0.02)
    global open_file
    open_file = Button(window2, text = 'Select File or Directory to Scan')
    open_file.bind("<Button-1>", open_file_browser)
    open_file.place(relx = 0.36, rely = 0.35)


    global next
    next = Button(window2, text = 'Next', command = scan_type_window)
    next.bind("<Button-1>")
    next.place(relx = 0.90, rely = 0.80)


def inc_progress_bar(percentage_complete):
    global progress_bar
    #This value will come from the number of bytes scanned at the moment the progress bar is called.
    progressBar['value'] = percentage_complete
    print 'fgdd', percentage_complete
    progressBar.update()

def create_scan_finished_button():
    global found_malware
    global window2
    global pause_button
    global resume_button
    global next
    pause_button.destroy()
    resume_button.destroy()

    print type(found_malware['text']), ': fm'
    if((found_malware['text']) != 0):
        next = Button(window2, text = 'Next', width = 10, command = action_page)
        next.configure(background = '#00cc44', fg = 'white')
        next.bind('<button-1>')
        next.place(relx = 0.44, rely = 0.87)

    elif((found_malware['text']) == 0):
        close = Button(window2, text = 'Close', width = 10, command = window2.destroy)
        close.configure(background = '#00cc44', fg = 'white')
        close.bind('<button-1>')
        close.place(relx = 0.46, rely = 0.87)


def scan_type_window():
    global  window2
    open_file.destroy()
    # window2 = Toplevel(window)
    # window2.geometry("800x300")
    # window2.configure(background = 'grey')
    # window2.title('Choose File or Directory to Scan')
    global integrity_check_bt
    global virus_scan_bt
    integrity_check_bt = Button(window2, text = 'Check file/directory \n for changes',  height = 10, width = 20, background = 'dark grey')
    integrity_check_bt.bind('<Button-1>')
    integrity_check_bt.place(relx = 0.22, rely = 0.20)

    virus_scan_bt = Button(window2, text = 'Virus Scan', height = 10, width = 20, background = 'dark grey', command = virus_scan_window)
    virus_scan_bt.bind('<Button-1>')
    virus_scan_bt.place(relx = 0.55, rely = 0.20)

def virus_scan_window():
    global window2
    global scanning
    global scanned_files
    integrity_check_bt.destroy()
    virus_scan_bt.destroy()

    background_image= PhotoImage(file="dki.png")
    background_label = Label(window2, image=background_image)
    background_label.image = background_image
    background_label.place(relx=0.43, rely=0.4, anchor=CENTER)

    print "initialise scanning"
    initialise_scanning()
    scanning = Label(window2, text = 'Scanning file: ')
    scanning.configure(background = 'grey', fg = 'white')
    scanning.place(relx = 0.02, rely = 0.10)
    global current_files_scanning

    global progressBar
    progressBar = ttk.Progressbar(window2, orient = HORIZONTAL, length = 890)
    progressBar.config(mode = 'determinate')
    progressBar.place(relx = 0.02, rely = 0.70)

    current_files_scanning = Label(window2, text = '', borderwidth=2, relief = 'raised')
    current_files_scanning.configure(background = 'grey')
    current_files_scanning.place(relx = 0.15, rely = 0.10)
    global number_of_files_scanned
    number_of_files_scanned = Label(window2, text = '', borderwidth=2, relief = 'groove')
    number_of_files_scanned.configure(background ='grey', fg = 'white', font = ('Helvetica', 30, 'bold'), width = 10)
    number_of_files_scanned.place(relx = 0.24, rely = 0.40)

    scanned_files = Label(window2, text='Scanned')
    scanned_files.configure(background = 'grey', fg = 'white')
    scanned_files.place(relx = '0.33', rely = '0.50')

    global found_malware
    found_malware = Label(window2, text = '', borderwidth = 2, relief = 'groove')
    found_malware.configure(background = 'grey', fg = 'white', font = ('Helvetica', 30, 'bold'), width = 10)
    found_malware.place(relx = '0.52', rely = '0.40')
    global found
    found = Label(window2, text='Found')
    found.configure(background = 'grey')
    found.place(relx = '0.62', rely = '0.50')

    global percentage_complete_label
    percentage_complete_label = Label(window2, text = '')
    percentage_complete_label.configure(background = 'grey')
    percentage_complete_label.place(relx = 0.02, rely = 0.65)

    global pause_button
    pause_button = Button(window2, text = 'Pause', width = 10)
    pause_button.bind('<button-1>')
    pause_button.configure(background = '#00cc44', fg = 'white', font = ('Helvetica', 12, 'bold'))
    pause_button.place(relx = 0.37, rely = 0.87)

    global resume_button
    resume_button = Button(window2, text = 'Resume', width = 10)
    resume_button.bind('<button-1>')
    resume_button.configure(background = '#00cc44', fg = 'white', font = ('Helvetica', 12, 'bold'))
    resume_button.place(relx = 0.52, rely = 0.87)

    progressBar['value'] = 0
    #This value will come from the number of bytes of the file or directory.
    progressBar['maximum'] = 100

    iterate_files()

def callback(event):
    print(treeview.selection())


def action_page():
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
    global treeview
    treeview = ttk.Treeview(window2)
    treeview.insert('', '0', 'item1', text = 'First Item')
    treeview.insert('', '1', 'item2', text = 'Second Item')
    treeview.column('#0', width = 150)
    treeview.heading('#0', text = 'Infected File')
    treeview.config(columns = ('File Path', 'Malware', 'Action Taken'))
    treeview.heading('File Path', text = 'File Path')
    treeview.heading('Malware', text = 'Malware Found')
    treeview.heading('Action Taken', text = 'Action Taken')
    treeview.bind('<<TreeviewSelect>>', callback)
    treeview.set('item1', 'Malware', 'Unix.Malware.Agent-1393500')
    treeview.place(relx = 0.30, rely = 0.20)



    delete_virus1 = Button(window2, text = 'Delete virus', command = delete_virus)
    delete_virus1.bind("<Button-1>")
    delete_virus1.place(relx = 0.10, rely = 0.30)

    quarantine = Button(window2, text = 'Quarantine', command = delete_virus)
    quarantine.configure(background = '#00cc44')
    quarantine.bind("<Button-1>")
    quarantine.place(relx = 0.10, rely = 0.45)





def create_configuration_window():


    global config_window
    config_window = Toplevel(window)
    config_window.title("Configuration")
    config_window.geometry("800x500")
    #==== Configuration page

    # logo3 = PhotoImage(file="Aware_logo3+.png")
    # logo3_label = Label(f3, image=logo3)
    # logo3_label.configure(background = 'black')
    # logo3_label.image  = logo3
    # logo3_label.place(relx=0.43, rely=0.4, anchor=CENTER)

    background_image= PhotoImage(file="background_scan_page.png")
    background_label = Label(config_window, image=background_image)
    background_label.image = background_image
    background_label.place(relx=0.43, rely=0.4, anchor=CENTER)


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

f6 = Frame(window)
f6.configure(background = "Black")
f6.grid_propagate(0)

f7 = Frame(window)
f7.configure(background = "Black")
f7.grid_propagate(0)

config_window = Toplevel(window)
window.configure(background = "Black")
date_update = Label(config_window, text = '')

for frame in (f1, f2, f3, f4, f5, f6, f7):
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

# def virus_scan_page()



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


# listbox = Listbox(f4, width = 65, height = 40)
# listbox.bind('<ButtonRelease-1>', Select_from_listbox)
# listbox.place(relx = 0.52, rely = 0.47)
#
# delete_virus = Button(f4, text = 'Delete virus', command = delete_virus)
# delete_virus.bind("<Button-1>")
# delete_virus.place(relx = 0.52, rely = 0.42)


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

# background_image= PhotoImage(file="background_scan_page.png")
# background_label = Label(f6, image=background_image)
# background_label.image = background_image
# background_label.place(relx=0.43, rely=0.4, anchor=CENTER)

logo5 = PhotoImage(file="Aware_logo3+.png")
logo5_label = Label(f6, image=logo5)
logo5_label.configure(background = 'black')
logo5_label.image  = logo5
logo5_label.place(relx=0.50, rely=0.10, anchor=CENTER)

logo6 = PhotoImage(file="antivirus_logo.png")
logo6_label = Label(f6, image=logo6)
logo6_label.configure(background = 'black')
logo6_label.image  = logo6
logo6_label.place(relx=0.50, rely=0.23, anchor=CENTER)

settings = PhotoImage(file = 'settings.png')
settings_logo = Label(f6, image = settings)
settings_logo.configure(background = 'black')
settings_logo.image = settings
settings_logo.place(relx = 0.10, rely = 0.60)

quarantine_image = PhotoImage(file = 'rsz_quarantine_file.png')
quarantine = Label(f6, image = quarantine_image)
quarantine.configure(background = 'black')
quarantine.image = quarantine_image
quarantine.place(relx = 0.33, rely = 0.60)

quarantine_button = Button(f6, text = 'Quarantine Logs')
quarantine_button.bind('<Button-1>')
quarantine_button.place(relx = 0.32, rely = 0.8)

file_scan_image = PhotoImage(file = 'rsz_file_scan.png')
file_scan = Label(f6, image = file_scan_image)
file_scan.configure(background = 'black')
file_scan.image = file_scan_image
file_scan.place(relx = 0.56, rely = 0.60)

file_scan_button = Button(f6, text = 'Scan Files', command = create_window)
file_scan_button.bind('<Button-1>')
file_scan_button.place(relx = 0.561, rely = 0.80 )

logs_image = PhotoImage(file = 'rsz_settings_logo.png')
logs = Label(f6, image = logs_image)
logs.configure(background = 'black')
logs.image = logs_image
logs.place(relx = 0.78, rely = 0.60)

file_scan_button = Button(f6, text = 'Settings', command = create_configuration_window)
file_scan_button.configure(background = 'Black', fg = 'light Blue')
file_scan_button.bind('<Button-1>')
file_scan_button.place(relx = 0.795, rely = 0.80 )

logged_in_as = Label(f6, text = 'logged in as: ')
logged_in_as.configure(background = 'black', fg = 'white')
logged_in_as.place(relx = 0.01, rely = 0.01)

raise_frame(f6)
window.mainloop()
