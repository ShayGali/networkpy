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

#### for example:

```
read_list, write_list, error_list = select.select([socket1, socket2, socket3], [socket1, socket2, socket3],
                                                  [socket1, socket2, socket3])
```

> [!IMPORTANT]
> the select function will block the program until one of the sockets in one of the lists is ready.

### our program
in our program we will use the select function to check if the server socket is ready for reading
the sockets that we will pass is:

1. the client_sockets list, so we will know when a client is ready to send a message
2. the server_socket, so we will know when a new client is trying to connect to the server

> Note: we can append the server_socket and the client_sockets to the same list as this: [server_socket] +
> client_sockets
