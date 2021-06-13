import os
from posix import PRIO_USER
from socket import * 


class Client():

    def __init__(self):
        self.client_address = 'localhost'
        self.client_port = 10000
        self.BUFFER_SIZE = 1024

    def create_socket(self, adrss, port) -> socket:
        client_socket = socket(AF_INET, SOCK_STREAM)  
        client_socket.connect((adrss, port))
        print("[CREATING] Client created!")
        return client_socket

    def receive_data(self, socket:socket):
        recived = socket.recv(self.BUFFER_SIZE ).decode()
        return recived

    def send_data(self, socket:socket,data:str):
        socket.send(data.encode())

    def close_socket(self, socket:socket):
        print("[QUIT] Closing client!")
        socket.close()

    def connect(self):
        client_socket = self.create_socket(self.client_address, self.client_port)
        print(self.receive_data(client_socket))
        while True:
            data = input("Input:")
            print("[SENDING] Request sended, waiting for server...")
            if data != '':
                if data == 'CLOSE':
                    self.close_socket(client_socket)
                    break
                if data.startswith('GET'):
            
                    self.send_data(client_socket,data)
                    if (self.receive_data(client_socket) == 'OK'):
                        print("[PROCESING] File exist, initializing transfer ....")
                        file_name = self.receive_data(client_socket)
                        file_name = os.path.basename(file_name)
                        self.save_file(file_name, client_socket)
                    else:
                        print("[ERROR] File doesnt exist!")
                        continue
                else:
                    self.send_data(client_socket,data)
                    received_data = self.receive_data(client_socket)
                    print(received_data)

    def save_file(self, file_name, client_socket):
        try:
            f = open(file_name, 'wb')
        except OSError:
            print("[ERROR] Error creating file")
        with f:
            while True:
                bytes_read = client_socket.recv(self.BUFFER_SIZE )
                print(f"[PROCESING]Receiving data...{len(bytes_read)}")
                f.write(bytes_read)
                if len(bytes_read) < self.BUFFER_SIZE:                                    
                    f.close()
                    print("[PROCESING] Data transfer ended...")
                    break 

     
if __name__ == '__main__':
    client = Client()
    client.connect()