
import os
from socket import * 


class Client():

    def __init__(self):
        self.client_address = 'localhost'
        self.client_port = 11000
        self.BUFFER_SIZE = 1024

    def create_socket(self, adrss, port) -> socket:
        client_socket = socket(AF_INET, SOCK_STREAM)  
        client_socket.connect((adrss, port))
        print("Socket cliente creado!")
        return client_socket

    def receive_data(self, socket:socket):
        recived = socket.recv(self.BUFFER_SIZE ).decode()
        return recived

    def send_data(self, socket:socket,data:str):
        socket.send(data.encode())

    def close_socket(self, socket:socket):
        socket.close()

    def connect(self):
        client_socket:socket = self.create_socket(self.client_address, self.client_port)
        print(self.receive_data(client_socket))
        while True:
            data = input("Ingrese comando:")
            if data != '':
                if data == 'CLOSE':
                    self.send_data(client_socket, data)
                    print(self.receive_data(client_socket))
                    print("Cerrando cliente...bye")
                    self.close_socket(client_socket)
                    break
                if data.startswith('GET'):
                    print("Peticion de transferencia enviada, esperando server...")
                    self.send_data(client_socket,data)
                    file_name = self.receive_data(client_socket)
                    file_name = os.path.basename(file_name)

                    try:
                        with open(file_name, 'wb') as f:

                            while True:
                                bytes_read = client_socket.recv(self.BUFFER_SIZE )
                                print(f"Recibiendo archivo...{len(bytes_read)}")
                                f.write(bytes_read)
                                if len(bytes_read) < self.BUFFER_SIZE:
                                    f.close()
                                    print("Transferencia finalizada")
                                    break                
                    except:
                        print("Error al solicitar archivo.")
                        continue
                else:
                    print("Mensaje enviado, esperando server...")
                    self.send_data(client_socket,data)
                    received_data = self.receive_data(client_socket)
                    print(f"\nRespuesta server:",received_data)

if __name__ == '__main__':
    client = Client()
    client.connect() 