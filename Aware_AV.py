from Tkinter import *
import check_login_details
import tkFileDialog
import register_user
import time
import file_integrity_check
from tkMessageBox import showinfo, showerror
import os
from multiprocessing.managers import State
import Aho_Corasick

count = 0
def raise_frame(frame):
    frame.tkraise()

def save_login_details(event):
    username1 = username.get()
    password1 = password.get()
    response = check_login_details.validate_credentials(str(username1), str(password1))
    if(response == True):
        showinfo("login success", "You have successfully logged in")
        raise_frame(f4)

def hide(event):
    event.widget.pack_forget()

def open_file_browser(event):
    file_browser = tkFileDialog.askopenfile(mode = 'r',  initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    print file_browser

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
    global count
    count = count + 1
    output.insert(END, "Scan in progress please wait... \n")
    time.sleep(2)
    if(count == 1):
        file_integrity_check.initialise()


    file_integrity_check.main("/home/nadia/Desktop/Third_Year_Project/", "Nadia23")
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
        quarantine = Button(f4, text = 'quarantine')
        quarantine.place(relx = 0.62, rely = 0.42)
        delete_virus = Button(f4, text = 'Delete virus')
        delete_virus.place(relx = 0.52, rely = 0.42)




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


window.configure(background = "Black")

for frame in (f1, f2, f3, f4):
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


variable = StringVar()
username = StringVar()
password = StringVar()
new_username = StringVar()
new_password = StringVar()
re_new_password = StringVar()
show_pass = BooleanVar()

logged_in_as_label = Label(f4, text = "logged in as: " + username.get());
logged_in_as_label.place(relx = 0.63, rely = 0.01 )

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
#dropdown.grid(column = 60, row = 3)

run = Button(f4, text = 'Run Virus Scan', command = open_program)
run.bind("<Button-1>")
run.place(relx = 0.08, rely = 0.42)

listbox = Listbox(f4, width = 65, height = 40)
listbox.place(relx = 0.52, rely = 0.47)




print username.get()
raise_frame(f3)
window.mainloop()
