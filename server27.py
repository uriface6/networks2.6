#   Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020

import socket
import protocol27 as protocol
import glob
import os
import shutil
import subprocess
import pyautogui


IP = '0.0.0.0'
PORT = 8820
PHOTO_PATH = r"C:\networks\works" # The path + filename where the screenshot at the server should be saved


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # Use protocol.check_cmd first
    # Then make sure the params are valid
    # (6)

    ## use in check_cmd function in protocol27

    return True, "DIR", ["c:\\cyber"]


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data
    """
    # (7)
    print("server command: " + command)

    if command == "dir":
        try:
            reply = ', '.join(glob.glob(params[0] + r'\\*.*'))
        except:
            reply = "dir error!"

    elif command == "delete":
        try:
            os.remove(params[0])
            reply = "delete successes"
        except:
            reply = "delete error!"

    elif command == "copy":
        try:
            shutil.copy(params[0], params[1])
            reply = "copy successes"
        except:
            reply = "copy error!!!"

    elif command == "execute":
        try:
            subprocess.call(params[0])
            reply = "execute successes"
        except:
            reply = "execute error"

    elif command == "take_screenshot":
        try:
            image = pyautogui.screenshot()
            image.save(r'C:\\networks\\works\\screen.jpg')
            reply = "screenshot successes"
        except:
            reply = "screenshot error!!!"

    elif command == "send_photo":
        try:
            file = open(r'C:\\networks\\works\\screen.jpg', mode='rb')  # b is important -> binary
            file_content = file.read()
            reply = str(len(file_content))
            print("file len: " + reply)
            file.close()
        except:
            reply = "send_photo error"

    elif command == "exit":
        reply = "goodBye"
    else:
        reply = "command error"

    return reply


def main():
    # open socket with client
    # (1)
    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Server is up and running")

    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        print("cmd: " + cmd)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = protocol.check_cmd(cmd)
            print("command: " + command)
            if valid_cmd:

                # (6)

                # prepare a response using "handle_client_request"
                # add length field using "create_msg"
                # send to client
                reply = handle_client_request(command, params)
                reply = protocol.create_msg(reply)
                client_socket.send(reply)
                print("server sent: " + reply.decode())

                if command == 'send_photo':
                    # Send the data itself to the client
                    # (9)!!!!!

                    try:
                        file = open(r'C:\\networks\\works\\screen.jpg', mode='rb')  # b is important -> binary
                        file_content = file.read()
                        print("!!!!!!!!!!!!!!!!")
                        print("file size: " + str(len(file_content)))
                        client_socket.send(file_content)
                        file.close
                    except:
                        print("send photo error")

                if command == 'exit':
                    break
            else:
                # prepare proper error to client
                reply = 'Bad command or parameters'
                # send to client
                reply = protocol.create_msg(reply)
                client_socket.send(reply)

        else:
            # prepare proper error to client
            reply = 'Packet not according to protocol'
            #send to client
            reply = protocol.create_msg(reply)
            client_socket.send(reply)
            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")


if __name__ == '__main__':
    main()
