from Tkinter import *
import check_login_details
import tkFileDialog
import register_user
import time
import file_integrity_check
from tkMessageBox import showinfo, showerror
import os
import Aho_Corasick
from multiprocessing.managers import State
import Aho_Corasick

count = 0


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
        raise_frame(f4)

def hide(event):
    event.widget.pack_forget()

def open_file_browser(event):
    file_path = tkFileDialog.askopenfile(mode = 'r',  initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    file_path = str(file_path).split(",")
    global file_path
    file_path =  file_path[0]
    global file_path
    file_path = file_path.split(" ")
    global file_path
    file_path =  file_path[2]

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

def delete_virus():
    print "filename: ", value
    file_name = value
    print file_name
    Aho_Corasick.main(file_name, "delete")


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

    file = open("infected_files.txt")
    for line in file:
         listbox.insert(END, line)
    file.close()

    #if infected files are found give option to delete of quarantine the files.
    any_files_infected = os.stat("infected_files.txt").st_size == 0
    if(any_files_infected == False):
        quarantine = Button(f4, text = 'quarantine', command = create_window())
        quarantine.place(relx = 0.62, rely = 0.42)


def create_window():
    window2 = Toplevel(window)
    window2.geometry("800x300")
    # open_file = Button(window2, text = 'open file')
    # open_file.bind("<Button-1>", open_file_browser)
    # open_file.place(relx = 0.001, rely = 0.02)
    open_file = Button(window2, text = 'Select File or Directory to Scan')
    open_file.bind("<Button-1>", open_file_browser)
    open_file.place(relx = 0.36, rely = 0.20)
    run = Button(window2, text = 'Run Virus Scan', command = open_program)
    run.bind("<Button-1>")
    run.place(relx = 0.42, rely = 0.40)




def create_configuration_window():
    config_window = Toplevel(window)
    config_window.title("Configuration")
    config_window.geometry("800x500")
    config_window.configure(background = 'white')


        #==== Configuration page

    deep_scan = BooleanVar()
    medium_scan = BooleanVar()
    shallow_scan = BooleanVar()
    email_results = BooleanVar()
    frequency = StringVar()

    config_label = Label(config_window, text = 'Configuration')
    config_label.config(background = 'White', font =('Courier', 30), fg = 'black')
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
    scanType.configure(background = 'white', fg = 'blue')
    scanType.place(relx = 0.01, rely = 0.31)

    checkbutton_scanType_deep = Checkbutton(config_window, text = "Deep", variable = deep_scan)
    checkbutton_scanType_deep.configure(background = 'white', fg = 'black')
    checkbutton_scanType_deep.place(relx= 0.01, rely= 0.36)


    checkbutton_scanType_medium = Checkbutton(config_window, text = 'medium', variable = medium_scan)
    checkbutton_scanType_medium.configure(background = 'white', fg = 'black')
    checkbutton_scanType_medium.place(relx= 0.16, rely= 0.36)


    checkbutton_scanType_shallow = Checkbutton(config_window, text = 'shallow', variable = shallow_scan)
    checkbutton_scanType_shallow.configure(background = 'white', fg = 'black')
    checkbutton_scanType_shallow.place(relx= 0.31, rely = 0.36)


    checkbutton_email = Checkbutton(config_window, text = 'Email scan results', variable = email_results)
    checkbutton_email.place(relx = 0.01, rely = 0.46)
    #checkbutton_email.configure(background = 'black', fg = 'white')

    virus_database_update_label = Label(config_window, text = 'Virus Database update: ')
    virus_database_update_label.configure(background = 'white', fg = 'blue')
    virus_database_update_label.place(relx = 0.01, rely = 0.56)

    manual_update = Button(config_window, text = 'Manual Update')
    manual_update.configure(background = 'white', fg = 'black')
    manual_update.place(relx = 0.01, rely = 0.61)
    #need to place and create variables for the checkbuttons.S

    or_label = Label(config_window, text = 'or')
    or_label.configure(background = 'white', fg = 'black')
    or_label.place(relx = 0.20, rely = 0.61)

    checkbutton_automatic_db_update = Checkbutton(config_window, text = 'Automatic Update')
    checkbutton_automatic_db_update.configure(background = 'white', fg = 'black')
    checkbutton_automatic_db_update.place(relx = 0.26, rely = 0.61)

    #===



window = Tk()
window.geometry("1100x700")
window.title("Aware Antivirus")
file_path = StringVar()



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





window.configure(background = "Black")

for frame in (f1, f2, f3, f4, f5, f6):
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

#c = Checkbutton(f1, text="Are you the admin?")
#c.configure(background = "Blue", fg = "white")
#c.grid(row = 1, column = 0)

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

username_label = Label(f1, text = "Username: ")
username_label.configure(background = "Black", fg = "white")
username_label.grid(row = 5, column = 0, sticky = W)
username_entry_path = Entry(f1, textvariable = username)
username_entry_path.grid(row = 5, column = 1)

password_label = Label(f1, text = "Password: ")
password_label.configure(background = "Black", fg = "white")
password_label.grid(row = 6, column = 0, sticky = W)
password_entry_path = Entry(f1, textvariable = password)
password_entry_path.grid(row = 6, column = 1)

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

submit_button = Button(f1, text = 'Submit')
submit_button.bind("<Button-1>", save_login_details)
submit_button.grid(row = 7, column = 1)

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

run = Button(f4, text = 'Run Virus Scan', command = open_program)
run.bind("<Button-1>")
run.place(relx = 0.08, rely = 0.42)

listbox = Listbox(f4, width = 65, height = 40)
listbox.bind('<ButtonRelease-1>', Select_from_listbox)
listbox.place(relx = 0.52, rely = 0.47)

delete_virus = Button(f4, text = 'Delete virus', command = delete_virus)
delete_virus.bind("<Button-1>")
delete_virus.place(relx = 0.52, rely = 0.42)


logged_in_as_label = Label(f4, text = "logged in as: " + username.get());
print password.get()
logged_in_as_label.place(relx = 0.63, rely = 0.01 )


configuration_button = Button(f4, text = 'Configuration', command = create_configuration_window)
configuration_button.bind('<Button-1>')
configuration_button.configure(font =('Courier'))
configuration_button.place(relx = 0.01 , rely = 0.01)

#=====: Front option page
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



print username.get()
raise_frame(f6)
window.mainloop()
