import socket
import struct
from logging import exception

my_socket = socket.socket()
my_socket.connect(('127.0.0.1', 8820))

exit_flag = False
msg2server = -1

while not exit_flag:

    msg2server = -1
    while msg2server < 0 or msg2server > 3:
        usr_cmd = input("enter command (TIME, WHORU, RAND, EXIT) : ")
        usr_cmd = usr_cmd.upper()

        if usr_cmd == "TIME":
            msg2server = 0
        elif usr_cmd == "WHORU":
            msg2server = 1
        elif usr_cmd == "RAND":
            msg2server = 2
        elif usr_cmd == "EXIT":
            msg2server = 3
            exit_flag = True
        else:
            print("command error!")

    msg2server = str(f"{len(str(msg2server)):02}") + str(msg2server)
    print(msg2server)
    my_socket.send(msg2server.encode())

    len_data = 99
    try:
        len_data = int(my_socket.recv(2).decode())
        data = my_socket.recv(len_data).decode()
    except exception:
        print("len of data error!!")
        data = ""
        my_socket.recv(1024)


    if data != "":
        print("the server sent: " + data)
    else:
        print("connection erorr")

my_socket.close()
