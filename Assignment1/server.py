import socket 
import select 
import sys
from thread import *  
"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""
IP_ADDRESS = '127.0.0.1'
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
  
""" 
binds the server to an entered IP address and at the 
specified port number. 
The client must be aware of these parameters 
"""
server.bind((IP_ADDRESS, PORT)) 
  
""" 
listens for 100 active connections. This number can be 
increased as per convenience. 
"""
server.listen(100) 
  
list_of_clients = [] 
list_of_usernames = []
  
def clientthread(conn, addr): 
	
    # Save the username and append it to the list.
    client_username = conn.recv(256).decode('UTF-8')
    list_of_usernames.append(client_username)

    # Print username and address of connected client
    print('User ' + client_username + ' connected. (' + addr[0] + ')')

    # sends a message to the client whose user object is conn 
    conn.send(('Welcome to this chatroom ' + client_username + '!\nType /exit at any time to disconnect.').encode('UTF-8')) 
  
    while True: 
            try: 
                message = conn.recv(2048).decode('UTF-8')

                # H
                if(message[0:8] == '/private'):
                    data = message.split(' ', 2)
                    if privatemessage(client_username, data[1], data[2]) == -1:
                        conn.send('User not found'.encode('UTF-8'))

                elif message: 
  
                    """prints the message and username of the 
                    user who just sent the message on the server 
                    terminal"""
                    print('<' + client_username + '> ' + message)
  
                    # Calls broadcast function to send message to all 
                    message_to_send = ("<" + client_username + "> " + message).encode('UTF-8')
                    broadcast(message_to_send, conn) 
  
                else: 
                    """message may have no content if the connection 
                    is broken, in this case we remove the connection"""
                    remove(conn) 
  
            except: 
                continue
  
"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message, connection): 
    for clients in list_of_clients: 
        try: 
            clients.send(message) 
        except: 
            clients.close() 

            # if the link is broken, we remove the client 
            remove(clients) 

""" This function is used when sending one-to-one private messages
between the clients. The function compares the receiver username to
the list_of_usernames and sends the private message when a match is found.
The indexes are the same on list_of_usernames and list_of_clients,
which is why the iteration is done by using index i. """
def privatemessage(sender_name, receiver_name, message):

    for i in range(0,len(list_of_clients)):
        print(i)
        if list_of_usernames[i] == receiver_name:
            try:
                message_to_send = ('<Private message from ' + sender_name + '> ' + message).encode('UTF-8')
                list_of_clients[i].send(message_to_send)
                print('<Private message from ' + sender_name + ' to ' + receiver_name + '> ' + message)
                return 0
            except:
                list_of_clients[i].close()
                break
    return -1

            


  
"""The following function simply removes the object 
from the list that was created at the beginning of  
the program"""
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
  
while True: 
  
    """Accepts a connection request and stores two parameters,  
    conn which is a socket object for that user, and addr  
    which contains the IP address of the client that just  
    connected"""
    conn, addr = server.accept()

  
    """Maintains a list of clients for ease of broadcasting 
    a message to all available people in the chatroom"""
    list_of_clients.append(conn) 
  
    # creates and individual thread for every user  
    # that connects 
    start_new_thread(clientthread,(conn,addr))     
  
conn.close() 
server.close() 

