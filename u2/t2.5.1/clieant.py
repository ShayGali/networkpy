import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect(("127.0.0.1", 8820))

while True:
    msg = input("Enter message (NAME | TIME | RAND): ")
    server_socket.send(msg.encode())
    res = server_socket.recv(1024).decode()
    print(res)

    if res == "BYE":
        break

server_socket.close()
