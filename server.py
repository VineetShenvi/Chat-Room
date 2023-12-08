import socket
import threading
from datetime import datetime
import sqlite3

PORT = 8800
SERVER = "127.0.0.1"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

clients, names = [], []

server = socket.socket()
server.bind(ADDRESS)

def startChat():

	print("server is working on " + SERVER)

	server.listen()

	while True:

		conn, addr = server.accept()
		conn.send("NAME".encode(FORMAT))

		name = conn.recv(1024).decode(FORMAT)

		names.append(name)
		clients.append(conn)

		print(f"Name is : {name}")
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")

		broadcastMessage(f"[{current_time}]\t{name} has joined the chat!".encode(FORMAT))

		# Start the handling thread
		thread = threading.Thread(target=handle,
								args=(conn, addr))
		thread.start()

		# no. of clients connected
		# to the server
		print(f"active connections {threading.active_count()-1}")

# method to handle the
# incoming messages


def handle(conn, addr):

	print(f"new connection {addr}")
	connected = True

	while connected:
		# receive message
		message = conn.recv(1024)

		# broadcast message
		broadcastMessage(message)

	# close the connection
	conn.close()

# method for broadcasting
# messages to the each clients


def broadcastMessage(message):
	for client in clients:
		client.send(message)

def create_user_info_table():
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

create_user_info_table()


# call the method to
# begin the communication
startChat()
