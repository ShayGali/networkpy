"""
This file is used to test the server by taking advantage of a weakness in the security of the code.
The weakness is that the server does not check if the user is already answer the question or not.
So, the client can send the same answer multiple times, and the server will count it as a correct answer.

In this file, we will create a client that will send the same answer multiple times, and will get a high score.
"""
import socket
import time

import lib.chatlib as chatlib

MAX_MSG_LENGTH = 1024
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5678

print("starting to attack the server...")

# Create socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect((SERVER_IP, SERVER_PORT))
print("connected to server")

# Login
username = "attacker"
password = "123456"
my_socket.send(
    chatlib.build_message(
        chatlib.PROTOCOL_CLIENT["login_msg"], f"{username}{chatlib.DATA_DELIMITER}{password}"
    ).encode()
)

# check if login success or not
cmd, data = chatlib.parse_message(my_socket.recv(MAX_MSG_LENGTH).decode())

if cmd != chatlib.PROTOCOL_SERVER["login_ok_msg"]:
    print(f"Login failed, the server send: {data}")
    exit(1)

print("Login successful")

# Get question
my_socket.send(chatlib.build_message(chatlib.PROTOCOL_CLIENT["get_question"], "").encode())

cmd, data = chatlib.parse_message(my_socket.recv(MAX_MSG_LENGTH).decode())

if cmd != chatlib.PROTOCOL_SERVER["get_question"]:
    print(f"Error getting question, the server send: {data}")
    exit(1)

q_id = data.split(chatlib.DATA_DELIMITER)[0]

# Send answer - we will send 1, just to check which answer is correct
my_socket.send(
    chatlib.build_message(chatlib.PROTOCOL_CLIENT["send_answer"], f"{q_id}{chatlib.DATA_DELIMITER}1").encode()
)

# Get answer result
cmd, data = chatlib.parse_message(my_socket.recv(MAX_MSG_LENGTH).decode())

correct_answer = 1

if cmd == chatlib.PROTOCOL_SERVER["error_msg"]:
    print(f"Error sending answer, the server send: {data}")
    exit(1)

if cmd != chatlib.PROTOCOL_SERVER["correct_answer"]:
    correct_answer = data

print("get question and send answer successful")

print("starting to send the same answer 100 times...")
# Send the same answer 100 times
for i in range(100):
    my_socket.send(
        chatlib.build_message(chatlib.PROTOCOL_CLIENT["send_answer"],
                              f"{q_id}{chatlib.DATA_DELIMITER}{correct_answer}").encode()
    )
    time.sleep(0.01)

print("sending the same answer 100 times successful")

print("flushing the server...")
# get all the server response and ignore them
for _ in range(100):
    data = my_socket.recv(MAX_MSG_LENGTH)  # Adjust buffer size as needed
    print(data.decode())
print("getting score...")
# Get score
my_socket.send(chatlib.build_message(chatlib.PROTOCOL_CLIENT["get_score_msg"], "").encode())

cmd, data = chatlib.parse_message(my_socket.recv(MAX_MSG_LENGTH).decode())

if cmd != chatlib.PROTOCOL_SERVER["get_score_msg"]:
    print(f"Error getting score, the server send: {data}")
    exit(1)

print(cmd)
print(f"Your score is: {data}")
print("the attack is successful")
print("closing the socket...")
my_socket.close()
print("socket closed")
