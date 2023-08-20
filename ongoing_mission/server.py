##############################################################################
# server.py
##############################################################################

import socket
from typing import Set, Dict, Tuple
from lib.objects import User, Question

import lib.chatlib as chatlib
import lib.printer as printer

# GLOBALS
"""
The users set and the questions dict are used to store the data of the server.
in the future, this data will be loaded from files, but for now, it is hardcoded.
"""
users: Dict[str, User] = {}  # a dist of all users (User objects), the key is the username
# a dict of questions, each question is a dict with the following fields: question, answers list, correct answer index (0-3). each key is a unique number, that represents a question
questions: Dict[int, Question] = {}  # a dist of all the questions (Question objects), the key is the question id
logged_users: Dict[str, User] = {}  # a dict of all the logged-in users (User objects), the key is the username

# CONSTANTS
ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def send_error(conn: socket.socket, error_msg: str) -> None:
    """
    Send error message with given message
    Receives: socket, message error string from called function
    Returns: None
    """
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], error_msg)


def build_and_send_message(conn: socket.socket, code: str, data: str) -> None:
    """
    Builds a new message using chatlib, wanted code and message.
    Prints [DEBUG] info, then sends it to the given socket.
    Parameters: conn (socket object), code (str), data (str)
    Returns: None
    """
    req = chatlib.build_message(code, data)
    printer.print_debug(f"[DEBUG-SERVER]: sending message: {req}")
    conn.send(req.encode())


def recv_message_and_parse(conn: socket.socket) -> Tuple[str, str]:
    """
    Receives a new message from given socket,
    then parses the message using chatlib.
    Parameters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occurred, will exit the program.
    """
    res = conn.recv(1024).decode()
    printer.print_debug(f"[DEBUG-CLIENT]: got message: {res}")

    cmd, data = chatlib.parse_message(res)
    if cmd is None:
        send_error(conn, "Error on parsing your message")

    if cmd == chatlib.PROTOCOL_SERVER["error_msg"]:
        send_error(conn, f"Error on receive your data. the data that received : {data}")

    return cmd, data


def build_send_recv_parse(conn: socket.socket, code: str, data: str) -> Tuple[str, str]:
    """
    Builds a new message using chatlib, wanted code and message.
    Prints [DEBUG] info, then sends it to the given socket.
    Then, receives a new message from given socket,
    then parses the message using chatlib.
    Parameters: conn (socket object), code (str), data (str)
    Returns: cmd (str) and data (str) of the received message.
    If error occurred, will return None, None
    """
    build_and_send_message(conn, code, data)
    return recv_message_and_parse(conn)


# Data Loaders #

def load_questions() -> Dict[int, Question]:
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Receives: -
    Returns: questions dictionary
    """
    questions_from_db = {
        2313: Question(2313, "How much is 2+2", ["3", "4", "2", "1"], 2),
        4122: Question(4122, "What is the capital of France?", ["Lion", "Marseille", "Paris", "Montpelier"], 3),

    }

    return questions_from_db


def load_user_database() -> Dict[str, User]:
    """
    Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
    Receives: -
    Returns: user set
    """
    users_from_db = {
        "test", User(1, "test", "test"),
        "yossi", User(2, "yossi", "123", 50),
        "master", User(3, "master", "master", 200),
    }
    return users_from_db


# SOCKET CREATOR

def setup_socket() -> socket.socket:
    """
    Creates new listening socket and returns it
    Receives: -
    Returns: the socket object
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen()

    printer.print_debug("[DEBUG]: Server is up, listening on port 5678...")

    return sock


##### MESSAGE HANDLING


def handle_get_score_message(conn, username):
    global users


def handle_logout_message(conn):
    """
    Closes the given socket (in later chapters, also remove user from logged_users dictionary)
    Receives: socket
    Returns: None
    """
    global logged_users


# Implement code ...


def handle_login_message(conn: socket.socket, data: str) -> None:
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Receives: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users  # To be used later

    username_password = chatlib.split_data(data, 2)  # Splitting the data to username and password

    # Check if the data parsed correctly
    if username_password is None:
        send_error(conn, "Error on parsing your credentials")
        return

    # get username and password from the data
    username = username_password[0]
    password = username_password[1]

    # check if the user exists, and if he does, check if the password is correct
    if username not in users or users[username].password != password:
        send_error(conn, "Wrong credentials")
        return

    # check if the user is already logged in
    if username in logged_users:
        send_error(conn, "User already logged in")
        return

    logged_users[username] = users[username]  # add user to logged users
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")  # send OK to client


def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Receives: socket, message code and data
    Returns: None
    """
    global logged_users  # To be used later


# Implement code ...


def main():
    # Initializes global users and questions dictionaries using load functions, will be used later
    global users
    global questions

    print("Welcome to Trivia Server!")


# Implement code ...


if __name__ == '__main__':
    main()
