import Tkinter as tk
from Carbon.QuickDraw import frame
LARGE_FONT = ("Verdana", 12)
#This method will always run when the class is called
#do not really have to pass self or the other parameters, it is just convention
#args: passing through variables, kwargs: passing through dictionaries. 
    
class intrusion_detection(tk.Tk):
    def __init__(self, *args, **kwargs ): 
        tk.Tk.__init__(self, *args, **kwargs)

     
        container = tk.Frame(self)

        container.pack(fill = None, expand = True)
        container.grid_rowconfigure(110, weight = 1)
        container.grid_columnconfigure(110, weight = 1)

        self.frames = {} #*
        
        for F in (LoginPage, add_file_page, test_page_3):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
        
        self.show_frame(LoginPage)
        
    def show_frame(self, cont):
        frame=self.frames[cont]
        frame.tkraise()
        
def print_out():
    print "woop"
    
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background = 'red')
        label = tk.Label(self, text = "log in page", font = LARGE_FONT)
        label.configure(bg = 'red')
        label.pack(pady =10, padx=10)
        log_in_button = tk.Button(self, text = "add_file_page", command =lambda: controller.show_frame(add_file_page))
        log_in_button.pack()
        page_3_button = tk.Button(self, text = "page_3", command =lambda: controller.show_frame(test_page_3))
        page_3_button.pack()
        entry_path = tk.Entry(self)
        entry_path.pack()

class add_file_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "add_file_page", font = LARGE_FONT)
        label.pack(pady =10, padx=10)
        back_button = tk.Button(self, text = "go back", command =lambda: controller.show_frame(LoginPage))
        back_button.pack()
        entry_path = tk.Entry(self)
        entry_path.pack()

class test_page_3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, background = 'red')
        back_button = tk.Button(self, text = "go back", command =lambda: controller.show_frame(LoginPage))
        back_button.grid(row = 4, column = 0)
        entry_path = tk.Entry(self)
        entry_path.grid(row = 1, column = 0)
        
app = intrusion_detection()
app.mainloop()
        
        