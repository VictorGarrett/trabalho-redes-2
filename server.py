import socket
import threading
import sys
import hashlib
import os

HOST = "10.0.0.16" 
PORT = 65433  

def listen(serversocket, stop_event):
    while not stop_event.is_set():
        try:
            c, addr = serversocket.accept()
            c.settimeout(1)
        except Exception as e:
            #print(f'exception on listen {e}')
            continue

        socket_map[addr] = c
        t = threading.Thread(target=client_recieve, args=(c, addr, messages, socket_map, stop_event))
        t.start()

def send_file(clientsocket, filename):  
    #print(f"sendfile {filename.decode('ascii')}---")
    try:
        with open(filename.decode('ascii'), 'rb') as file:
            size = os.path.getsize(filename)
            #print(f'sending file of size{size}')
            clientsocket.sendall(b'fbeg' + size.to_bytes(4, byteorder='big') + filename)
            md5 = hashlib.md5()
            chunk = file.read(1024)
            while chunk:
                md5.update(chunk)
                clientsocket.sendall(chunk)
                chunk = file.read(1024)
                
        clientsocket.sendall(b'fend' + md5.digest())
    except:
        clientsocket.sendall(b'text' + b'NO SUCH FILE!')

def send(messages, socket_map, stop_event):
    while not stop_event.is_set():
        if len(messages) > 0:
            msg = messages.pop()
            for addr, socket in socket_map.items():
                if msg[0] != addr:
                    socket.sendall(b'text'+ msg[1])

def client_recieve(clientsocket, addr, messages, socket_map, stop_event):
    clientsocket.setblocking(1)
    received_text = ''

    while received_text != 'exit' and not stop_event.is_set():
        try:
            msg = clientsocket.recv(1024)
            if len(msg) > 0:
                #print (f"{addr} >>  {msg}")

                if msg[0:7] == b'arquivo':
                    send_file(clientsocket, msg[8:])
                elif msg != 'exit':
                    messages.append((addr, msg))
                    print(msg.decode('ascii'))
                #clientsocket.sendall(msg)
                #print(messages)
            else:
                break
        except Exception as e:
            #print(f'exception on recv: {e}')
            continue
    #print("closing socket")
    clientsocket.close()
    del socket_map[addr]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))        # Bind to the port
s.listen()                 # Now wait for client connection.
s.settimeout(1)

stop_event = threading.Event()

messages = []
socket_map = {}

sender_thread = threading.Thread(target=send, args=(messages, socket_map, stop_event))
sender_thread.start()

running = True

listen_thread = threading.Thread(target=listen, args=(s, stop_event))
listen_thread.start()

while running:
   
    try:
        x = input()  
        #print(x)
        if x == 'exit':
            running = False
        else:
            messages.append((None, str.encode(x)))
    except Exception as e:
        #print(f'exception on main: {e}')
        running = False


stop_event.set()
listen_thread.join()
#print('thread joined')
s.close()
