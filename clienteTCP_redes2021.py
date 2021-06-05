from socket import * # Importo la libreria Sockets

class Client():

    def __init__(self) -> None:
        self.client_socket = socket(AF_INET, SOCK_STREAM)

        #Defino el objeto socket con los protocolos IPV4 y TCP.
    def connect(self):
        host = ('localhost',12000)
        self.client_socket.connect(host)
        print(f"Coneccion establecida en {host}")
        while True:
            sentence = input("Ingrese string a revertir:")
            if sentence!='':
                self.client_socket.send(sentence.encode('utf-8'))
                modified_sentence = self.client_socket.recv(1024).decode('utf-8')
                if (modified_sentence!=''):
                    print(f"Mensaje recibido: {modified_sentence}")
                else:
                    print("Mensaje enviado, esperando server...")
                    
if __name__ == '__main__':
    client = Client()
    client.connect()