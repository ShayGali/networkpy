import socket
import random
from typing import Dict, Tuple, Union, List

import select

from lib.objects import User, Question

import lib.chatlib as chatlib
import lib.printer as printer
import lib.db_handler as db

# GLOBALS
"""
The users set and the questions dict are used to store the data of the server.
in the future, this data will be loaded from files, but for now, it is hardcoded.
"""
users: Dict[str, User] = {}  # a dist of all users (User objects), the key is the username

questions: Dict[int, Question] = {}  # a dist of all the questions (Question objects), the key is the question id

# a dict of all the logged-in users (User objects), the key is the connection info (IP, port)
logged_users: Dict[Tuple[str, str], str] = {}

# a list of all the client sockets
client_sockets: List[socket.socket] = []

# a list of all the messages that need to be sent to the clients - (client socket, message)
messages_to_send: List[Tuple[Tuple[str, str], str]] = []

# CONSTANTS
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
    Builds a new message using chatlib. the message will be in the format of the protocol.
    the message for sending will append to the messages_to_send list,
    and will be sent when the socket is ready to write.
    Prints [DEBUG] info, then sends it to the given socket.
    Parameters: conn (socket object), code (str), data (str)
    Returns: None
    """
    global messages_to_send
    req = chatlib.build_message(code, data)
    printer.print_debug(f"[DEBUG-SERVER]: sending message: {req}")

    # append the message to the messages_to_send list
    messages_to_send.append((conn.getpeername(), req))


def recv_message_and_parse(conn: socket.socket) -> Union[Tuple[str, str], Tuple[None, None]]:
    """
    Receives a new message from given socket,
    then parses the message using chatlib.
    Parameters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occurred, will return None, None
    """
    # get the message from the socket
    res = conn.recv(1024).decode()
    printer.print_debug(f"[DEBUG-CLIENT]: got message: {res}")

    # check if the message is empty
    if res == "":
        return None, None

    # parse the message
    cmd, data = chatlib.parse_message(res)

    # check if the message parsed correctly
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
    Loads questions bank from file
    Receives: -
    Returns: questions dictionary
    """
    return db.get_all_questions()


def load_user_database() -> Dict[str, User]:
    """
    Loads users list from file
    Receives: -
    Returns: user dictionary
    """
    return db.get_all_users()


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


# ~~~ MESSAGE HANDLING ~~~ #

def handle_login_message(conn: socket.socket, data: str) -> None:
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Receives: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users  # To check if the user is already logged in, and to add him to the logged users dict
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
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_failed_msg"], "Wrong credentials")
        return

    # check if the user is already logged in
    if username in logged_users.values():
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_failed_msg"], "User already logged in")
        return

    logged_users[conn.getpeername()] = username  # add user to logged users dict
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")  # send OK to client


def handle_logout_message(conn: socket.socket) -> None:
    """
    Closes the given socket. removes user from logged_users, and removes the socket from client_sockets
    Receives: socket
    Returns: None
    """
    global logged_users
    global client_sockets

    del logged_users[conn.getpeername()]
    client_sockets.remove(conn)
    conn.close()


def handle_get_score_message(conn: socket.socket, username: str) -> None:
    """
    Gets username and send the score to the client.
    :param conn:
    :param username:
    :return:
    """
    global users

    current_user = users[username]
    score = current_user.score
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["get_score_msg"], str(score))


def handle_highscore_message(conn: socket.socket) -> None:
    global users
    sorted_by_score = sorted(users.values(), key=lambda u: u.score, reverse=True)
    res = "\n".join(map(lambda user: f"{user.username}: {user.score}", sorted_by_score))
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["get_high_score_msg"], res)


def get_login_players(conn: socket.socket) -> None:
    """
    Gets the logged in players and send them to the client.
    :param conn:
    :return:
    """
    global logged_users
    res = ", ".join(logged_users.values())
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["get_login_players_msg"], res)


def create_random_question() -> str:
    """
    Creates a random question from the questions' dictionary.
    The question will be in the format of the protocol.
    the format is: question_id#question#answer1#answer2#answer3#answer4#correct_answer
    :return: Question
    """
    global questions

    random_question: Question = random.choice(list(questions.values()))
    return random_question.format_to_send()


def handle_get_question(conn: socket.socket) -> None:
    """
    Gets a random question from the questions dictionary and send it to the client.
    :param conn:
    :return:
    """
    global questions
    global logged_users

    random_question = create_random_question()
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["get_question"], random_question)


def handle_send_answer(conn: socket.socket, data: str) -> None:
    """
    Gets the answer from the client and checks if it is correct.
    If the answer is correct, the user will get 5 points.
    :param conn:
    :param data:
    :return:
    """
    global questions
    global logged_users
    global users

    # check if the data parsed correctly
    id_choice = chatlib.split_data(data, 2)
    if id_choice is None:
        send_error(conn, "Error on parsing your answer")
        return
    if not (id_choice[0].isdigit() and id_choice[1].isdigit()):
        send_error(conn, "Error: if and choice must be numbers")
        return

    # get question id and choice, and if its valid
    q_id = int(id_choice[0])
    if q_id not in questions:
        send_error(conn, "Error: question id not exists")
        return

    choice = int(id_choice[1])
    q = questions[q_id]

    if choice < 1 or choice > 4:
        send_error(conn, "Error: choice must be between 1-4")
        return

    # check if the answer is correct, and send the response to the client
    if choice == q.correct:
        users[logged_users[conn.getpeername()]].score += 5
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["correct_answer"], "")
    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["wrong_answer"], str(q.correct))


def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command.
    if the user is not logged in, the only commands he can use are login.
    if the user is logged in, he can use all the commands, except login.

    Receives: socket, message code and data
    Returns: None
    """
    global logged_users  # To be used later

    if cmd is None:
        send_error(conn, "Error on parsing your message")
        return

    # if the command is login, we check if the user is already logged in
    if cmd == chatlib.PROTOCOL_CLIENT["login_msg"]:
        if conn.getpeername() in logged_users:
            send_error(conn, "You are already logged in!")
            return
    else:  # if the command is not login, we check if the user is logged in
        if conn.getpeername() not in logged_users:
            send_error(conn, "You are not logged in!")
            return

    if cmd == chatlib.PROTOCOL_CLIENT["login_msg"]:
        handle_login_message(conn, data)
    elif cmd == chatlib.PROTOCOL_CLIENT["logout_msg"]:
        handle_logout_message(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["get_score_msg"]:
        handle_get_score_message(conn, logged_users[conn.getpeername()])
    elif cmd == chatlib.PROTOCOL_CLIENT["get_high_score_msg"]:
        handle_highscore_message(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["get_login_players"]:
        get_login_players(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["get_question"]:
        handle_get_question(conn)
    elif cmd == chatlib.PROTOCOL_CLIENT["send_answer"]:
        handle_send_answer(conn, data)
    else:
        send_error(conn, "Unknown command")


def save_data():
    """
    Saves the users and questions to the database.
    :return:
    """
    global users
    global questions
    for user in users.values():
        db.save_user(user)
    for question in questions.values():
        db.save_question(question)


def main():
    # Initializes global users and questions dictionaries using load functions, will be used later
    global users
    global questions
    global client_sockets
    global messages_to_send

    # load the users and questions from the database
    users = load_user_database()
    questions = load_questions()

    print("Welcome to Trivia Server!")

    # set up the socket
    server_socket = setup_socket()

    # main loop
    while True:
        # get the sockets that are ready to read, write (error sockets are ignored for now)
        ready_to_read, ready_to_write, _ = select.select([server_socket] + client_sockets, client_sockets, [])

        # handle all the messages that need to be read
        for current_socket in ready_to_read:
            if current_socket is server_socket:  # if the socket is the server socket, we need to accept the new client
                (client_socket, client_address) = current_socket.accept()
                printer.print_debug(f"[DEBUG]: New client joined! {client_address}")
                client_sockets.append(client_socket)
            else:  # if the socket is a client socket, we need to read the message
                try:  # try to read the message
                    cmd, data = recv_message_and_parse(current_socket)
                except ConnectionResetError:  # if the client disconnected, we need to handle it
                    printer.print_debug(f"[DEBUG]: Client {current_socket.getpeername()} disconnected")
                    handle_logout_message(current_socket)
                    continue

                # if the client send an empty message, we need to handle it
                if data is None:
                    printer.print_debug(f"[DEBUG]: Connection {current_socket.getpeername()} closed!")
                    handle_logout_message(current_socket)
                else:  # if the client send a valid message, we need to handle it
                    printer.print_debug(f"[DEBUG]: client  {current_socket.getpeername()}, send: {data}")
                    handle_client_message(current_socket, cmd, data)

        # send all the messages that need to be sent
        for socket_to_write in ready_to_write:
            for message_to_send in messages_to_send:
                if message_to_send[0] == socket_to_write.getpeername():
                    socket_to_write.send(message_to_send[1].encode())
                    messages_to_send.remove(message_to_send)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:  # if an error occurred, we need to save the data before we exit
        save_data()
        raise e
