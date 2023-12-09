import socket
import threading
import sqlite3
from datetime import datetime
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox

 
PORT = 8800
SERVER = "127.0.0.1"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
 
client = socket.socket()
client.connect(ADDRESS)
 
class GUI:

    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()
 
        self.login = Toplevel()
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
 
        self.usernameEntry = Entry(self.login,
                               font="Helvetica 14")
 
        self.usernameEntry.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)
 
        self.usernameEntry.focus()

        self.passwordEntry = Entry(self.login,
                               font="Helvetica 14")
 
        self.passwordEntry.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.40)
 
        self.loginButton = Button(self.login,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=lambda: self.aunthenticate(self.usernameEntry.get(), self.passwordEntry.get()))
 
        self.loginButton.place(relx=0.15,
                      rely=0.6)
        
        self.registerButton = Button(self.login,
                         text="REGISTER",
                         font="Helvetica 14 bold",
                         command=lambda: self.register(self.usernameEntry.get(), self.passwordEntry.get()))
 
        self.registerButton.place(relx=0.5,
                      rely=0.6)
        self.Window.mainloop()
 
    def aunthenticate(self, username, password):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_info WHERE username = ? AND password = ?", (username, password))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            self.login.destroy()
            self.layout(username)
    
            rcv = threading.Thread(target=self.receive)
            rcv.start()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self, username, password):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_info (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "New user created successfully!")

    def layout(self, name):
 
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)
 
        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")
 
        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)
 
        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)
 
        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)
 
        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)
 
        self.labelBottom.place(relwidth=1,
                               rely=0.825)
 
        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")
 
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)
 
        self.entryMsg.focus()
 
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))
 
        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)
 
        self.textCons.config(cursor="arrow")
 
        scrollbar = Scrollbar(self.textCons)

        scrollbar.place(relheight=1,
                        relx=0.974)
 
        scrollbar.config(command=self.textCons.yview)
 
        self.textCons.config(state=DISABLED)
 
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()
 
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
 
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END,
                                         message+"\n\n")
 
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                print("An error occurred!")
                client.close()
                break
 
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            message = (f"[{current_time}]\t{self.name}: {self.msg}")
            client.send(message.encode(FORMAT))
            break

g = GUI()