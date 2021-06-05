from socket import *

class Server():

    def __init__(self):
        self.server_address = 'localhost'
        self.server_port = 14000

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
        socket.send(data.encode())

    def close_socket(self, socket:socket):
        socket.close()

    def connect(self):
        server_socket:socket = self.create_socket(self.server_address, self.server_port)      
        client_socket, address = server_socket.accept()
        print(f"Conexion establecida con exito en {address}")
        while True:
            print("Esperando al cliente")
            data = self.receive_data(client_socket)
            if(data!=''):
                if(data == 'quit'):
                    self.send_data('Server finalizado...',client_socket)
                    self.close_socket(client_socket)
                    print("Cerrando server...Bye")
                    break
                else:
                    print(f"Mensaje recibido: {data}")
                    self.send_data(data,client_socket)
                    print("Respuesta enviada!")
            

if __name__ == '__main__':

    server = Server()
    server.connect()   