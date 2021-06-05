
from socket import * 


class Client():

    def __init__(self):
        self.client_address = 'localhost'
        self.client_port = 12000

    def create_socket(self, adrss, port) -> socket:
        client_socket = socket(AF_INET, SOCK_STREAM)  
        client_socket.connect((adrss, port))
        print("Socket cliente creado!")
        return client_socket

    def receive_data(self, socket:socket) -> str:
        message = socket.recv(1024).decode()
        return message

    def send_data(self, socket:socket,data:str):
        socket.send(data.encode())

    def close_socket(self, socket:socket):
        socket.close()

    def connect(self):
        client_socket:socket = self.create_socket(self.client_address, self.client_port)
        print(self.receive_data(client_socket))
        while True:
            data = input("Ingrese comando:")
            if data == 'QUIT':
                self.send_data(client_socket, data)
                print(self.receive_data(client_socket))
                print("Cerrando cliente...bye")
                self.close_socket(client_socket)
                break 
            else:
                print("Mensaje enviado, esperando server...")
                self.send_data(client_socket,data)
                received_data = self.receive_data(client_socket)
                print(f"\nRespuesta server:",received_data)
                    
     
if __name__ == '__main__':
    client = Client()
    client.connect()