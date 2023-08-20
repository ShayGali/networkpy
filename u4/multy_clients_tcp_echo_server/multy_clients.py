import socket

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = '127.0.0.1'

num_of_clients = input("Enter number of clients: ")
if not num_of_clients.isdigit() or int(num_of_clients) <= 0:
    print("Invalid input")
    exit(1)

num_of_clients = int(num_of_clients)
sockets = []
for i in range(num_of_clients):
    sockets.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    sockets[i].connect((SERVER_IP, SERVER_PORT))

while True:
    i = input(f"Enter socket number [0-{num_of_clients - 1}]: ")

    if not i.isdigit() or int(i) < 0 or int(i) >= num_of_clients:
        break

    msg = input("Enter message (for close connection enter empty message) : ")
    sockets[int(i)].send(msg.encode())
    data = sockets[int(i)].recv(MAX_MSG_LENGTH).decode()
    print(f"Server response: {data}")
    if msg == "":
        sockets[int(i)].close()
        sockets.remove(sockets[int(i)])
        num_of_clients -= 1

for s in sockets:
    s.close()

print("all sockets closed!")
