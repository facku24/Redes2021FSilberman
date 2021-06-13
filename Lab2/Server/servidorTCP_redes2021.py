from posix import listdir
from posixpath import join, split
from socket import *
import os
from os.path import isfile
import threading
from datetime import datetime, timezone

class Server():

    def __init__(self):
        self.server_address = '0.0.0.0'
        self.server_port = 14000
        self.BUFFER_SIZE = 1024
        self.current_files=[]
        self.clients = []

    def create_socket(self, adrss, port) -> socket:
        server_socket = socket(AF_INET, SOCK_STREAM)  
        server_socket.bind((adrss, port))
        print("[STARTING] Server created...")
        return server_socket

    def receive_data(self, socket:socket):
        recived = socket.recv(self.BUFFER_SIZE).decode()
        return recived

    def send_data(self, data, socket:socket):
        socket.send(data.encode())

    def close_socket(self, socket:socket):
        print(self.save_msj(str("[CLOSING] Closing connection with client"+socket.getsockname())))
        socket.close()

    def connection(self, client_socket, addr):
        self.scan()
        self.send_data(f"[CONECTING] CONNECTED WITH SERVER {self.server_address, self.server_port}",client_socket)
        while True:
            try:
                print("[PROCESING] Waiting for client...")
                data = self.receive_data(client_socket).split(' ')
                if(len(data)!=0):
                    print(self.save_msj(str(f"[PROCESING] Message from  {addr}  :  {data}")))
                    if data == 'CLOSE':
                        self.close_socket(client_socket)
                        break
                    if data[0] in self.cases:
                        if len(data)==1:
                            try:
                                self.send_data(self.cases[data[0]](self),client_socket)
                            except KeyError:
                                print("KeyError!")
                        if len(data)==2:
                            try:
                                file_name = data[1]
                                self.cases[data[0]](self, file_name ,client_socket)
                            except:
                                pass
                    else:
                        self.send_data(f"[ERROR] Invalid input! \nComand list: {list(self.cases)}",client_socket)
                else:
                    self.send_data('[ERROR] No input detected!', client_socket)
            except IOError:
                self.close_socket(client_socket)
                self.update_clients(addr)
                break
    #Handling multiple clients (5) with Threading library.            
    def start(self,max_clients):
        server_socket:socket = self.create_socket(self.server_address, self.server_port)
        server_socket.listen(max_clients)
        while 1:
            connection_socket, addr = server_socket.accept()
            thread = threading.Thread(target = self.connection, args=(connection_socket, addr))
            self.update_clients(addr)
            thread.start()

    def update_clients(self, addr):

        if addr in self.clients:
            print(self.save_msj(str(f"[DISCONECTING] Ending connection with {addr}")))
            self.clients.remove(addr)
        else:
            print (self.save_msj(str(f"[CONNECTING] New client connected {addr}")))
            self.clients.append(addr)
            print(f"[PROCESING] Clients connected : {len(self.clients)}")
    
    def list_method(self):

        path = os.path.dirname(os.path.realpath(__file__))
        self.current_files = [obj for obj in listdir(path) if isfile(join(path , obj))]

        files = '\n[PROCESING] Directory files: \n'

        for file in self.current_files:

            files = files + '|---------'+str(file) +'\n'
            
        return files

    def get_method(self,file_name,client_socket:socket):
        if self.check(file_name):
            self.send_data('OK',client_socket) 
            print("[PROCESING] File founded!")
            self.send_data(file_name,client_socket)
            try:
                f = open(file_name,'rb')
            except OSError:
                print ("[ERROR] Could not open/read file:", file_name)
            with f:
                while True:
                    print(f"[PROCESING] Sending data to {client_socket.getsockname()} ...")
                    bytes_read = f.read(self.BUFFER_SIZE)
                    client_socket.sendall(bytes_read)
                    if not bytes_read:
                        print("[PROCESING] File sended!")
                        f.close()
                        break
        else:
            self.send_data('NON OK',client_socket)

    def metadata_method(self, file_name ,client_socket):
        print("Metadata!")
        stat_result = os.stat(file_name)
        modified = datetime.fromtimestamp(stat_result.st_mtime, tz=timezone.utc)
        last_access = datetime.fromtimestamp(stat_result.st_atime, tz=timezone.utc)
        size = stat_result.st_size
        meta = (f'Last time access: {last_access} \nLast time modified: {modified} \nSize in bytes: {size}')
        print(meta)
        self.send_data(meta,client_socket)
    # This function search for all files in server directory and update them in current_files..
    def scan (self):
        path = os.path.dirname(os.path.realpath(__file__))
        self.current_files = [obj for obj in listdir(path) if isfile(join(path , obj))]
        return path
    # This functions checks if exists the file in the current_files
    def check (self, file_name):
        self.scan()
        return file_name in self.current_files

    def save_msj(self, message):
        try:
            f = open('historial.txt', 'a')
            with f:
                f.write (message + '\n')
                f.close()
        except:
            print("[ERROR] Error during saving data from client")
        return message

    cases = {

    'LIST': list_method,
    'CLOSE': None,
    'GET': get_method,
    'METADATA': metadata_method

    }

            
if __name__ == '__main__':

    server = Server()
    server.start(5)   