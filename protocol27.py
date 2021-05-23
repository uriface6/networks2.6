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
    data_list = data.split()

    command = data_list[0].lower()
    if command == "dir" and len(data_list) == 2:
        cmd_flag = True
    elif command == "delete" and len(data_list) == 2:
        cmd_flag = True
    elif command == "copy" and len(data_list) == 3:
        cmd_flag = True
    elif command == "execute" and len(data_list) == 2:
        cmd_flag = True
    elif command == "take_screenshot":
        cmd_flag = True
    else:
        cmd_flag = False

    return cmd_flag


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
        msg = "Erorr"
        my_socket.recv(1024)
        msg_flg = False

    return msg_flg, msg


