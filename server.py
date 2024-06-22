import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65433  # Port to listen on (non-privileged ports are > 1023)

def on_new_client(clientsocket,addr):
    
    received_text = ''

    while received_text != 'exit'
    msg = clientsocket.recv(1024)
    #do some checks and if msg == someWeirdSignal: break:
    print (f"{addr} >>  {msg}")
    #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
    clientsocket.sendall(msg)
    clientsocket.close()

s = socket.socket()         # Create a socket object



s.bind((HOST, PORT))        # Bind to the port
s.listen()                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   t = threading.Thread(target=on_new_client, args=(c, addr))
   t.start()
   #Note it's (addr,) not (addr) because second parameter is a tuple
   #Edit: (c,addr)
   #that's how you pass arguments to functions when creating new threads using thread module.
s.close()