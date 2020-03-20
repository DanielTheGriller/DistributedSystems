""" Daniel Linna
    0509355
    28.2.2020   """

""" Help to general structure of the application got from
https://www.geeksforgeeks.org/simple-chat-room-using-python/"""
import socket 
import select 
import sys
from thread import *  


IP_ADDRESS = '0.0.0.0'
PORT = 8080
HELP_MESSAGE = '\nCommands:\n\n/private username message\t\tto send private messages\n/joinchannel channelname\t\tto join a channel\n/leavechannel channelname\t\tto leave a channel\n/channel channelname message\t\tto send message to a channel\n/exit\t\t\t\t\tto exit the system\n\nList of channels:\n\nchannel1\nchannel2\nchannel3'

# Server configurations
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server.bind((IP_ADDRESS, PORT)) 

# Listen to max 100 clients, it will probably be enough for this
server.listen(100) 
  
""" Define different lists for later use
list_of_clients stores all the client connections
list_of_usernames stores all the usernames in a way
that the index matches the one with list_of_clients.
channelX_users contains the user connections of that 
channel """
list_of_clients = [] 
list_of_usernames = []
channel1_users = []
channel2_users = []
channel3_users = []
  
def clientthread(conn, addr): 
	
    # Save the username and append it to the list.
    client_username = conn.recv(256).decode('UTF-8')
    list_of_usernames.append(client_username)

    # Print username and address of connected client
    print('User ' + client_username + ' connected. (' + addr[0] + ')')

    # Sends a message to the client whose user object is conn 
    conn.send(('Welcome to this chatroom ' + client_username + '!\nType /exit at any time to disconnect.\nType /help for help.').encode('UTF-8')) 
  
    while True: 
            try: 
                message = conn.recv(2048).decode('UTF-8')

                # Handle private messages
                if(message[0:8] == '/private'):
                    data = message.split(' ', 2)
                    if privatemessage(client_username, data[1], data[2]) == -1:
                        conn.send('User not found'.encode('UTF-8'))
                # When user wants to join a channel
                elif(message[0:12] == '/joinchannel'):
                    data = message.split(' ', 1)
                    if joinchannel(data[1].strip(), conn) == -1:
                        conn.send('Channel not found'.encode('UTF-8'))
                # When user wants to leave a channel   
                elif(message[0:13] == '/leavechannel'):
                    data = message.split(' ', 1)
                    if leavechannel(data[1].strip(), conn) == -1:
                        conn.send('Channel not found'.encode('UTF-8'))
                # When user sends a message to a channel
                elif(message[0:8] == '/channel'):
                    data = message.split(' ', 2)
                    if channelmessage(conn, client_username, data[1].strip(), data[2]) == -1:
                        conn.send('Channel not found'.encode('UTF-8'))
                # When user triggers help
                elif(message.strip() == '/help'):
                    message_to_send = HELP_MESSAGE.encode('UTF-8')
                    conn.send(message_to_send)
                # If user wants to send message to everyone
                elif message: 
                    print('<' + client_username + '> ' + message)
  
                    # Call function broadcast to send the message to everyone
                    message_to_send = ("@all<" + client_username + "> " + message).encode('UTF-8')
                    broadcast(message_to_send, conn) 
  
                else: 
                    """if connection is broken, remove the user with remove function
                    and also from list_of_usernames. Print to server-side when user has
                    been disconnected. """
                    print('User ' + client_username + ' disconnected.')
                    remove(conn) 
                    list_of_usernames.remove(client_username)
                    return
  
            except: 
                continue
  
"""This function is used when broadcasting the message to all 
clients. There is no restrictions in whom to send the message. """
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


""" This function is used when sending messages to a channel."""
def channelmessage(connection, sender_name, channel, message):
    if checkuserchannel(channel, connection):
        if channel == 'channel1':
            sendlist = channel1_users
            message_to_send = ('@channel1 <' + sender_name + '> ' + message).encode('UTF-8')
        elif channel == 'channel2':
            sendlist = channel2_users
            message_to_send = ('@channel2 <' + sender_name + '> ' + message).encode('UTF-8')
        elif channel == 'channel3':
            sendlist = channel3_users
            message_to_send = ('@channel3 <' + sender_name + '> ' + message).encode('UTF-8')
        else:
            return -1
        for connection in sendlist:
            try:
                connection.send(message_to_send)
                print(message_to_send.decode('UTF-8'))
            except:
                connection.close()
                remove(connection)
    else:
        connection.send('You are not in that channel'.encode('UTF-8'))


""" This function checks if user is added on a channel """
def checkuserchannel(channel, connection):
    if channel == 'channel1':
        checklist = channel1_users
    elif channel == 'channel2':
        checklist = channel2_users
    elif channel == 'channel3':
        checklist = channel3_users
    else:
        return -1
    for user in checklist:
        if user == connection:
            return 1
    return 0


""" This function simply adds the connection to the
list of the selected channel. This allows user to receive
channel-specific messages. """          
def joinchannel(channel, connection):
    if checkuserchannel(channel, connection):
        connection.send('You are already at that channel.'.encode('UTF-8'))
        return 0
    if channel == 'channel1':
        channel1_users.append(connection)
    elif channel == 'channel2':
        channel2_users.append(connection)
    elif channel == 'channel3':
        channel3_users.append(connection)
    else:
        return -1
    return 0


""" This function removes user from selected channel list.
This way user does not receive that channel's messages anymore. """
def leavechannel(channel, connection):
    if checkuserchannel(channel, connection):
        if channel == 'channel1':
            channel1_users.remove(connection)
        elif channel == 'channel2':
            channel2_users.remove(connection)
        elif channel == 'channel3':
            channel3_users.remove(connection)
        else:
            return -1
        return 0
    else:
        connection.send('You are not in that channel'.encode('UTF-8'))
        


  
"""The following function simply removes the client object 
from the list of clients. """
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 

  
while True: 
  
    """ Accepting a connection and storing two parameters,
    connection and address. """
    conn, addr = server.accept()

  
    """Maintains a list of clients """
    list_of_clients.append(conn) 
  
    """ creates and individual thread for every user  
    that connects """ 
    start_new_thread(clientthread,(conn,addr))     
  
conn.close() 
server.close() 

