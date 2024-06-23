import socket
import threading
import hashlib
import os

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65433  # The port used by the server

def print_received(messages, s):
    while True:
        data = s.recv(1024)
        if data[0:4] == b'text':
            print(data[4:].decode('ascii'))
        elif data[0:4] == b'fbeg':
            md5 = hashlib.md5()
            filename = data[4:]
            recvfile = open(filename, 'wb')
        elif data[0:4] == b'fprt':
            recvfile.write(data[4:])
            md5.update(data[4:]) 
        elif data[0:4] == b'fend':
            received_hash = data[4:]
            calc_hash = md5.digest()

            recvfile.close()
            if received_hash != calc_hash:
                print('Failed to receive file!')
                os.remove(filename)
            


messages = []



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    
    text = ''
    s.connect((HOST, PORT))
    t = threading.Thread(target=print_received, args=(messages, s))
    t.start()
    while text != 'exit':
        text = input()
        s.sendall(str.encode(text))

#print(f"Received {data!r}")