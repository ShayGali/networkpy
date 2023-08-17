import socket
import sys

from typing import Tuple

import lib.chatlib as chatlib  # To use chatlib functions or consts, use chatlib.****
import lib.printer as printer

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def connect() -> socket.socket:
    """
    Connect to the given server, return the open socket.
    :return: socket object
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((SERVER_IP, SERVER_PORT))
    printer.print_debug("[DEBUG]: connected to server")
    return server_socket


def build_and_send_message(conn: socket.socket, code: str, data: str) -> None:
    """
    Builds a new message using chatlib, wanted code and message.
    Prints [DEBUG] info, then sends it to the given socket.
    Parameters: conn (socket object), code (str), data (str)
    Returns: None
    """
    req = chatlib.build_message(code, data)
    printer.print_debug(f"[DEBUG]: sending message: {req}")
    conn.send(req.encode())


def recv_message_and_parse(conn: socket.socket) -> Tuple[str, str]:
    """
    Receives a new message from given socket,
    then parses the message using chatlib.
    Parameters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occurred, will return None, None
    """
    res = conn.recv(1024).decode()
    printer.print_debug(f"[DEBUG]: got message: {res}")

    cmd, data = chatlib.parse_message(res)
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


def error_and_exit(error_msg: str) -> None:
    """
    Prints given error message, closes the program with error code 1
    :param error_msg: error message to print
    :return: None
    """
    print(error_msg, file=sys.stderr)
    exit()


def login(conn: socket.socket) -> None:
    """
    Tries to log in user to server.
    get user and password from user and send to server.

    :param conn: socket object to communicate with server
    :return: None
    """
    while True:
        # get user and password from user
        # username = input("Please enter username: ")
        # password = input("Please enter password: ")
        username = password = "test"
        # build data in the right format
        data = chatlib.join_data([username, password])

        # build and send message, and then parse the response
        cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["login_msg"], data)

        # check if login success or not
        if cmd == chatlib.PROTOCOL_SERVER["login_ok_msg"]:
            print("Login successful")
            return
        elif cmd == chatlib.PROTOCOL_SERVER["login_failed_msg"]:
            print("Login failed")
        else:
            error_and_exit("Login failed due to unexpected response from server")


def logout(conn: socket.socket) -> None:
    """
    Logs out user from server.
    :param conn:
    :return: None
    """
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")


def get_score(conn: socket.socket) -> None:
    """
    Gets score from server.
    :param conn:
    :return: None
    """
    cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_score_msg"], "")
    if cmd == chatlib.PROTOCOL_SERVER["your_score_msg"]:
        print(f"Your score is: {data}")
    else:
        error_and_exit("Error getting score")


def get_high_score(conn: socket.socket) -> None:
    """
    Gets high score from server.
    :param conn:
    :return: None
    """
    cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_high_score_msg"], "")
    if cmd == chatlib.PROTOCOL_SERVER["get_high_score_msg"]:
        print(f"High score is:\n{data}")
    else:
        error_and_exit("Error getting high score")


def play_question(conn: socket.socket) -> None:
    """
    Gets new question from the server,and print it to the user.
    Then get the user answer, and send it to the server.
    If the answer is correct, the server send CORRECT_ANSWER.
    If the answer is wrong, the server send WRONG_ANSWER.
    We print the response to the user.

    If the server send NO_QUESTIONS, the game is end.
    If error occurred, the program will close.

    TODO: split the function to smaller functions
    :param conn:
    :return:
    """

    # get question from server
    cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_question"], "")

    # check if the game is ended
    if cmd == chatlib.PROTOCOL_SERVER["no_questions"]:
        print("No more questions to you")
        return
    # check if the server send the question
    elif cmd == chatlib.PROTOCOL_SERVER["get_question"]:
        # split the data to question and answers
        split_data = chatlib.split_data(data, 6)

        # check if the data is valid
        if split_data is None:
            error_and_exit("Error play question - number of field is not 6")

        # gets question ID and question
        q_id = split_data[0]
        q = split_data[1]

        # print the question and answers
        print(f"Q: {q}\n\t1. {split_data[2]}\n\t2. {split_data[3]}\n\t3. {split_data[4]}\n\t4. {split_data[5]}")

        # get user answer and check if it valid
        user_ans = input("\nYou answer is [1-4]: ")

        if not user_ans.isdigit() or int(user_ans) < 1 or int(user_ans) > 4:
            printer.print_error("Invalid Input")

        # send answer to server and get response
        cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["send_answer"],
                                          chatlib.join_data([q_id, user_ans]))

        # check if the answer is correct or not, and print the response
        if cmd == chatlib.PROTOCOL_SERVER["correct_answer"]:
            printer.print_ok("Correct")
        elif cmd == chatlib.PROTOCOL_SERVER["wrong_answer"]:
            printer.print_with_color(f"Wrong! the correct answer is: {data}", printer.PURPLE)
        else:
            error_and_exit("Error play question - get response on the answer")
    # if the server send wrong response
    else:
        error_and_exit("Error play question - get wrong response")


def main():
    """
    Main method.
    connect to server, login, logout, and close connection.
    """
    conn = connect()
    login(conn)
    user_input = ""
    while user_input != "q":
        user_input = input("Please choose one of the following options:\n"
                           "p\t Play a trivia question\n"
                           "s\t Get my score\n"
                           "h\t Get the high score\n"
                           "q\t Quit\n")

        if user_input == "p":
            play_question(conn)
        elif user_input == "s":
            get_score(conn)
        elif user_input == "h":
            get_high_score(conn)
        elif user_input != "q":
            print("Invalid input")

    logout(conn)
    conn.close()
    printer.print_debug("[DEBUG]: connection closed")


if __name__ == '__main__':
    main()
