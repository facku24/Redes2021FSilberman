from posix import listdir
from posixpath import join
from socket import *
import os
from os.path import isfile

class Server():

    def __init__(self):
        self.server_address = 'localhost'
        self.server_port = 12000
        self.current_files=[]

    def create_socket(self, adrss, port) -> socket:
        server_socket = socket(AF_INET, SOCK_STREAM)  
        server_socket.bind((adrss, port))
        server_socket.listen(1)
        print("Servidor creado exitosamente!")
        return server_socket

    def receive_data(self, socket:socket):
        message = socket.recv(1024).decode()
        return message

    def send_data(self, data:str, socket:socket):
        data = str(data)
        socket.send(data.encode())

    def close_socket(self, socket:socket):
        socket.close()

    def connect(self):
        server_socket:socket = self.create_socket(self.server_address, self.server_port)      
        client_socket, address = server_socket.accept()
        self.send_data(f'Conectado al server en {self.server_address, self.server_port}',client_socket)
        print(f"Conexion establecida con exito en {address}")
        while True:
            print("Esperando al cliente")
            data = self.receive_data(client_socket)
            if(data!=''):
                print(f"Mensaje cliente: {data}")
                if data == 'QUIT':
                    print("Cerrando server...bye!")
                    self.send_data('Servidor finalizado',client_socket)
                    self.close_socket(server_socket)
                    break
                if data in self.cases:
                    try:
                        self.send_data(self.cases[data](self),client_socket)
                    except KeyError:
                        print("KeyError! ")
                else:
                    self.send_data(f"Comando no valido!\nLista de comandos: {list(self.cases)}",client_socket)
            else:
                self.send_data('Ingreso un valor!', client_socket)
        
    def list_method(self):
        #Ruta de la direccion actual.
        path = os.path.dirname(os.path.realpath(__file__))

        #Lista de los archivos en esta ruta, los guardo por si los necesito mas luego.
        
        dir =[obj for obj in listdir(path) if isfile(join(path , obj))]
        self.current_files = dir

        print(f"Directory files: {dir}")

        files = 'Archivos en el directorio:\n'

        for file in dir:

            files = files + str(file) +'\n'
            
        return files

    #Auxiliar function for tests
    def invert(self,data):
        return data[::-1]
 
    cases = {
        
    'LIST': list_method,
    'QUIT': None
     
    }
            

if __name__ == '__main__':

    server = Server()
    server.connect()   