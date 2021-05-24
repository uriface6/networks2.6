#   Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020


import socket
import protocol27 as protocol


IP = '127.0.0.1'
PORT = 8820
SAVED_PHOTO_LOCATION = r"C:\networks\works" # The path + filename where the copy of the screenshot at the client should be saved

def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    # (8) treat all responses except SEND_PHOTO

    # (10) treat SEND_PHOTO
    if cmd == "send_photo":
        #need to add
        flag, msg = protocol.get_msg(my_socket)
        if msg == "send_photo error":
            print(msg)
        else:
            try:
                file_size = int(msg)
                print(file_size)
                read_file = my_socket.recv(file_size)
                write_file = open(r'C:\\networks\\works\\client_screen.jpg', mode='wb')  # b is important -> binary
                write_file.write(bytearray(read_file))
                write_file.close()

            except:
                print("error to open file")
                my_socket.recv(1024)

    else:
        flag, msg = protocol.get_msg(my_socket)
        print(msg)

def main():
    # open socket with the server
    # (2)
    my_socket = socket.socket()
    my_socket.connect((IP, PORT))

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            packet = protocol.create_msg(cmd)
            my_socket.send(packet)
            print("client send: " + packet.decode())
            handle_server_response(my_socket, cmd)
            if cmd == 'exit':
                break
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()

if __name__ == '__main__':
    main()