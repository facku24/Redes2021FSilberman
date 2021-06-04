from socket import * # Importo la libreria Sockets

#Defino el objeto socket con los protocolos IPV4 y TCP.
client_socket = socket(AF_INET, SOCK_STREAM)

client_socket.connect(('localhost',8000))

print(client_socket.recv(1024).decode('utf-8'))

while True:

    sentence = input("Ingrese string a revertir:")

    if sentence!='':
        client_socket.send(sentence.encode('utf-8'))
        modified_sentence = client_socket.recv(1024).decode('utf-8')
        print(f"Mensaje recibido: {modified_sentence}")


