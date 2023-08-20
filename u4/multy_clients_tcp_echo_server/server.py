import socket
import select

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = '0.0.0.0'


def print_client_sockets(client_sockets):
    print("Connected clients:")
    for i, c in enumerate(client_sockets):
        print(
            f"\t{i + 1}. {c.getpeername()}")  # getpeername() returns the (ip, port) of the client connected to the socket


def main():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()

    print("Listening for clients...")
    client_sockets = []  # list of all the client sockets that are connected to the server

    while True:  # wait for clients, and handle them one by one
        # get sockets that are ready to be read from
        ready_to_read, _, _ = select.select([server_socket] + client_sockets, [], [])
        # handle each socket that is ready to be read from
        for current_socket in ready_to_read:
            # if the socket is the server socket - there is a new client that wants to connect
            if current_socket is server_socket:
                (client_socket, client_address) = current_socket.accept()
                print(f"New client joined! {client_address}")
                client_sockets.append(client_socket)
                print_client_sockets(client_sockets)
            # else, the socket is a client socket - a client sent a message
            else:
                print(f"New data from client {current_socket.getpeername()}")
                data = current_socket.recv(MAX_MSG_LENGTH).decode()
                if data == "":
                    print("Connection closed", )
                    client_sockets.remove(current_socket)
                    current_socket.close()
                    print_client_sockets(client_sockets)
                else:
                    print(f"cliect send: {data}")
                    current_socket.send(data.encode())


if __name__ == '__main__':
    main()
