from Tkinter import *
import check_login_details
import tkFileDialog
import register_user
from tkMessageBox import showinfo, showerror
from multiprocessing.managers import State
import Aho_Corasick

def raise_frame(frame):
    frame.tkraise()

def save_login_details(event):
    username1 = username.get()
    password1 = password.get()
    response = check_login_details.validate_credentials(str(username1), str(password1))
    if(response == True):
        showinfo("login success", "You have successfully logged in")
        raise_frame(f4)
        
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
    output1 =  Aho_Corasick.main()
    output.insert(END, output1)


               
window = Tk()
window.geometry("850x500")
window.title("Aware Antivirus")

f3 = Frame(window)
f3.configure(background = "Black")
f3.grid_propagate(0)

f1 = Frame(window, width = 1000, height = 500)
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

login_label = Label(f1, text = "Login:")
login_label.grid(row = 0, column = 0, sticky = W)
login_label.configure(background = "Black", fg = "White")

register_label = Label(f2, text = "   Register:")
register_label.grid(row =0, column = 10, sticky = W)
register_label.configure(background = "Black", fg = "White")

#c = Checkbutton(f1, text="Are you the admin?")
#c.configure(background = "Blue", fg = "white")
#c.grid(row = 1, column = 0)

select_login = Button(f3, text = 'Login', command= lambda:raise_frame(f1))
select_login.grid(row = 0, column = 0, columnspan = 10, sticky = E)

select_register = Button(f3, text = 'Register', command= lambda:raise_frame(f2))
select_register.grid(row = 3, column = 11)

variable = StringVar()
username = StringVar()
password = StringVar()
new_username = StringVar()
new_password = StringVar()
re_new_password = StringVar()
show_pass = BooleanVar()

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

back_to_login_page_button = Button(f2, text='Go back', command= lambda:raise_frame(f1))
back_to_login_page_button.grid(row = 0, column = 0)

output = Text(f4, width = 50, height = 20)
output.grid(column = 0, row = 0)



open_file = Button(f4, text = 'open file')
open_file.bind("<Button-1>", open_file_browser)
open_file.grid(row = 2, column = 30)
dropdown = OptionMenu(f4, variable, "file1", "file2", "file3")
dropdown.configure(background = "Black")
dropdown.grid(column = 0, row = 3)

run = Button(f4, text = 'Run', command = open_program)
run.bind("<Button-1>")
run.configure(background = "Black")
run.grid(row = 30, column = 0)

raise_frame(f3)
window.mainloop()