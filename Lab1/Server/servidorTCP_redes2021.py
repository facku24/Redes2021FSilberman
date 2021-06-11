from posix import listdir
from posixpath import join, split
from socket import *
import os
from os.path import isfile

class Server():

    def __init__(self):
        self.server_address = 'localhost'
        self.server_port = 13000
        self.BUFFER_SIZE = 1024
        self.current_files=[]

    def create_socket(self, adrss, port) -> socket:
        server_socket = socket(AF_INET, SOCK_STREAM)  
        server_socket.bind((adrss, port))
        server_socket.listen(1)
        print("Servidor creado exitosamente!")
        return server_socket

    def receive_data(self, socket:socket):
        recived = socket.recv(self.BUFFER_SIZE).decode()
        return recived

    def send_data(self, data, socket:socket):
        socket.send(data.encode())

    def close_socket(self, socket:socket):
        socket.close()

    def connect(self):
        server_socket:socket = self.create_socket(self.server_address, self.server_port)      
        client_socket, address = server_socket.accept()
        path = os.path.dirname(os.path.realpath(__file__))
        self.current_files = [obj for obj in listdir(path) if isfile(join(path , obj))]
        self.send_data(f'Conectado al server en {self.server_address, self.server_port}',client_socket)
        print(f"Conexion establecida con exito en {address}")
        while True:
            print("Esperando al cliente")
            data = self.receive_data(client_socket).split(' ')
            if(len(data)!=0):
                print(f"Mensaje cliente: {data}")
                if data == 'CLOSE':
                    print("Cerrando server...bye!")
                    self.send_data('Servidor finalizado',client_socket)
                    self.close_socket(server_socket)
                    break
                if data[0] in self.cases:
                    print(f"Entrada correcta de CASO {data[0]}")
                    if len(data)==1:
                        try:
                            self.send_data(self.cases[data[0]](self),client_socket)
                        except KeyError:
                            print("KeyError!")
                    if len(data)==2:
                        try:
                            file_name = data[1]
                            self.cases[data[0]](self, file_name,client_socket)
                        except:
                            pass
                else:
                    self.send_data(f"Comando no valido!\nLista de comandos: {list(self.cases)}",client_socket)
            else:
                self.send_data('Ingrese un valor!', client_socket)
        
    def list_method(self):

        path = os.path.dirname(os.path.realpath(__file__))
        self.current_files = [obj for obj in listdir(path) if isfile(join(path , obj))]

        print(f"\nDirectory files: {self.current_files}")

        files = '\nARCHIVOS EN EL DIRECTORIO: \n'

        for file in self.current_files:

            files = files + str(file) +'\n'
            
        return files

    def get_method(self,file_name,client_socket:socket):
        print(file_name)
        print(self.current_files)
        if file_name in self.current_files:
            print("El archivo existe en este directorio!")
            file_size = os.path.getsize(file_name)
            self.send_data(f"{file_name}",client_socket)
            print(f"Tamaño del archivo: {file_size}")
            with open(file_name,'rb') as f:
                while True:
                    print("Enviando...")
                    bytes_read = f.read(self.BUFFER_SIZE)
                    client_socket.sendall(bytes_read)
                    if not bytes_read:
                        print("Archivo enviado!")
                        f.close()
                        break
                
        else:
            return "\nArchivo inexistente"

    def metadata_method(self):
        return "\nFunction not implemented yet..."

 
    cases = {

    'LIST': list_method,
    'CLOSE': None,
    'GET': get_method,
    'METADATA': metadata_method

    }

            
if __name__ == '__main__':

    server = Server()
    server.connect()   