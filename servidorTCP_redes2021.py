from socket import * # Importo la libreria Sockets

class Server():


    #Direccion del servidor... ('red', 'puerto')
    def __init__(self):
        self.server_address = ('localhost', 12000)
        #Defino el objeto socket con los protocolos IPV4 y TCP.
        self.server_socket = socket(AF_INET, SOCK_STREAM)

    def create(self) -> bool:
            self.server_socket.bind(self.server_address)
            self.server_socket.listen(5)
            print("Servidor creado exitosamente!")
    def connect(self):
        client_socket, address = self.server_socket.accept()
        print(f"Conexion establecida con exito en {address}")
        while True:
            message=''
            print("Esperando al cliente")
            message = client_socket.recv(1024).decode()
            if(message!=''):
                print(f"Mensaje reibido: {message}")
                client_socket.send(self.invertString(message).encode())


    #Funcion auxiliar para invertir cadenas
    def invertString(self,elem:str):
        return elem[::-1]

if __name__ == '__main__':

    server = Server()
    server.create()
    server.connect()   