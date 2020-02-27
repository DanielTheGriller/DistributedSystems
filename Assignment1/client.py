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
  
    """ There are two possible input situations. Either the 
    user wants to give  manual input to send to other people, 
    or the server is sending a message  to be printed on the 
    screen. Select returns from sockets_list, the stream that 
    is reader for input. So for example, if the server wants 
    to send a message, then the if condition will hold true 
    below.If the user wants to send a message, the else 
    condition will evaluate as true"""
    read_sockets, write_socket, error_socket = select.select(sockets_list,[],[]) 
  
    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048).decode('UTF-8')
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

