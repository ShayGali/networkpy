import socket
import time
import random

SERVER_NAME = "TASK 1"

# initialize server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 8820))
server_socket.listen(5)
print("server is up and running")


# Wait for a connection
def generate_response(data: str) -> str:
    pass


client_socket, client_address = server_socket.accept()
print(f"Connected to {client_address}")

while True:
    # Receive data from the client
    data = client_socket.recv(1024).decode()

    print(f"Client send: {data}")

    if not data or data == "Quit":
        client_socket.send("BYE".encode())
        break

    response = "Not valid command"

    if data == "TIME":
        response = time.ctime()
    elif data == "NAME":
        response = SERVER_NAME
    elif data == "RAND":
        response = str(random.randint(1, 10))

    client_socket.send(response.encode())

client_socket.close()
print(f"Disconnected from {client_address}")
