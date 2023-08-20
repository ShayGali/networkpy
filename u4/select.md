# select function

### What is the select function?

we can handel <u>multiple clients</u> at a time by using select function.</br>
the select function tracks multiple sockets and determines which one is ready for reading or writing.</br>

### Input

**select function takes <u>3 lists as arguments:</u>**

1. the first list is the list of sockets that we want to check if they are **ready for reading**
2. the second list is the list of sockets that we want to check if they are **ready for writing**
3. the third list is the list of sockets that we want to check if they **have an error**

### Output

**the select function <u>returns 3 lists:</u>**

1. the first list is the list of sockets that are **ready for reading**
2. the second list is the list of sockets that are **ready for writing**
3. the third list is the list of sockets that **have an error**

##### for example:

```
read_list, write_list, error_list = select.select([socket1, socket2, socket3], [socket1, socket2, socket3],
                                                  [socket1, socket2, socket3])
```

#### ready_to_write

the select function will return the sockets that are ready for writing when we try to send a message to a client.
so we can use the select function to check if the socket is ready for writing before we send a message to the client.

if there is a socket that dont ready for writing, we can append it to a list and try to send the message again later.

**for example:**
we will initialize a list that will contain a tuple of the socket and the message that we want to send to the
client, ```messages_to_send```</br>
when we want to send a message to a client we will append the socket and the message to the ```messages_to_send```
list (`messages_to_send.append((current_socket, data))`).</br>
then we will use the select function to check if the socket is ready for writing.</br>
and then we will loop over the ```messages_to_send``` list and try to send the message to the client if he is in
the ```ready_to_write``` list.

```python
for message in messages_to_send:
    current_socket, data = message
    if current_socket in ready_to_write:
        current_socket.send(data.encode())
        messages_to_send.remove(message)
```

if the client is not ready, the message will be sent later.


> [!IMPORTANT]
> the select function will block the program until one of the sockets in one of the lists is ready.

### our program

in our program we will use the select function to check if the server socket is ready for reading
the sockets that we will pass is:

1. the client_sockets list, so we will know when a client is ready to send a message
2. the server_socket, so we will know when a new client is trying to connect to the server

> Note: we can append the server_socket and the client_sockets to the same list as this: [server_socket] +
> client_sockets
