import socket
from datetime import datetime
import random
from logging import exception

server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 8820))
server_socket.listen()
print("Server is up and running")

(client_socket, client_address) = server_socket.accept()
print("Client connected")

exit_flag = False

while not exit_flag:

    len_data = 99
    try:
        len_data = int(client_socket.recv(2).decode())
        data = client_socket.recv(len_data).decode()
        print("Client sent: " + data)
    except exception:
        print("len of data error!!")
        data = ""
        client_socket.recv(1024)

    if data == "0":
        reply = str(datetime.now())
    elif data == "1":
        reply = "my name is UriServer"
    elif data == "2":
        reply = str(random.randint(1, 10))
    elif data == "3":
        reply = "Goodbye!!!"
        exit_flag = True
    else:
        reply = "Command error"

    reply = str(f"{len(reply):02}") + reply
    client_socket.send(reply.encode())

client_socket.close()
server_socket.close()