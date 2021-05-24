import os.path
#   Ex. 2.7 template - protocol


LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """

    # (3)
    cmd_flag = False
    data_list = data.split(" ", 1)
    param = []

    command = data_list[0].lower()
    print("check_command: " + command + " len: " + str(len(data_list)))
    if command == "dir" and len(data_list) == 2:
        if os.path.exists(data_list[1]):
            cmd_flag = True
            param.append(data_list[1])
        else:
            print("dir error!!!")
    elif command == "delete" and len(data_list) == 2:
        if os.path.isfile(data_list[1]):
            cmd_flag = True
            param.append(data_list[1])
        else:
            print("delete error!!!")
    elif command == "copy" and len(data_list) == 2:
        data_list = data.split(" ")
        if len(data_list) == 3 and os.path.isfile(data_list[1]): #and os.path.isfile(data_list[2])
            cmd_flag = True
            param.append(data_list[1])
            param.append(data_list[2])
    elif command == "execute" and len(data_list) == 2:
        print("im executing!!!")
        if os.path.isfile(data_list[1]):
            cmd_flag = True
            param.append(data_list[1])
        else:
            print("execute error!!!")
    elif command == "take_screenshot" and len(data_list) == 1:
        cmd_flag = True
    elif command == "send_photo" and len(data_list) == 1:
        cmd_flag = True
    elif command == "exit" and len(data_list) == 1:
        cmd_flag = True
    else:
        cmd_flag = False

    return cmd_flag, command, param


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """

    # (4)
    return (str(f"{len(str(data)):04}") + data).encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    # (5)

    msg_flg = False
    msg = ""

    try:
        len_data = int(my_socket.recv(4).decode())
        msg = my_socket.recv(len_data).decode()
        msg_flg = True
    except:
        print("len of data error!!")
        msg = "Error"
        my_socket.recv(1024)
        msg_flg = False

    return msg_flg, msg

"""
def get_dir_from_file_path(file_path):
    path_list = file_path.split(r"\\\\")
    dir_path = ""
    for path in path_list[0:-2]:
        dir_path += path

    return dir_path
"""
