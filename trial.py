import sqlite3
from tkinter import *
from tkinter import font
from tkinter import ttk

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()
 
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300)
        
        self.usernameLabel = Label(self.login,
                               text="Username: ",
                               font="Helvetica 15")
 
        self.usernameLabel.place(relheight=0.2,
                             relx=0.1,
                             rely=0.15)
        
        self.passwordLabel = Label(self.login,
                               text="Password: ",
                               font="Helvetica 15")
 
        self.passwordLabel.place(relheight=0.2,
                             relx=0.1,
                             rely=0.35)
 
        # create a entry box for
        # tyoing the message
        self.usernameEntry = Entry(self.login,
                               font="Helvetica 14")
 
        self.usernameEntry.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)
 
        # set the focus of the cursor
        self.usernameEntry.focus()

        self.passwordEntry = Entry(self.login,
                               font="Helvetica 14")
 
        self.passwordEntry.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.40)
 
        # create a Continue Button
        # along with action
        self.loginButton = Button(self.login,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get()))
 
        self.loginButton.place(relx=0.15,
                      rely=0.6)
        
        self.registerButton = Button(self.login,
                         text="REGISTER",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get()))
 
        self.registerButton.place(relx=0.5,
                      rely=0.6)
        self.Window.mainloop()

GUI()