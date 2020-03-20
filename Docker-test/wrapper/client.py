""" Daniel Linna
    0509355
    28.2.2020   """

""" Help to general structure of the application got from
https://www.geeksforgeeks.org/simple-chat-room-using-python/"""
import socket 
import select 
import sys 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

username = str(raw_input('Enter your username: '))
IP_ADDRESS = str(raw_input('Enter IP address: '))
PORT = 8080

server.connect((IP_ADDRESS, PORT)) 
server.send(username.encode('UTF-8'))

  
while True: 
  
    # maintains a list of possible input streams 
    sockets_list = [sys.stdin, server]
  
    """ There are only two types of input. User entering manual
    input to server, and server sending input back to client. There
    are also commands for example /private but those are handled on
    server-side, except the /exit which will close the connection from
    client side. """
    r_sockets, w_socket, e_socket = select.select(sockets_list,[],[]) 
  
    for s in r_sockets: 
        if s == server: 
            message = s.recv(2048).decode('UTF-8')
            print(message) 
        else: 
            message = sys.stdin.readline() 
            
            # If user types /exit, close the server and exit program.
            if(message.strip() == '/exit'):
                print('Disconnecting from chat.')
                server.close()
                sys.exit()

            server.send(message) 


server.close() 

