from socket import * # Importo la libreria Sockets

#Funcion auxiliar para invertir cadenas
def invertString(elem:str):
    return elem[::-1]
#Defino el objeto socket con los protocolos IPV4 y TCP.
server_socket = socket(AF_INET, SOCK_STREAM) 

#Vinculo el socket creado a la red local, en el puerto 8000
server_socket.bind(('localhost',8000))

#Cola de espera que tendra el socket...
server_socket.listen(5)


print("Servidor creado exitosamente")
#Establezco conexion con el socket del cliente, guardo su ddireccion...
client_socket, direccion = server_socket.accept()
print(f"Conexion establecida con {direccion}")
client_socket.send(bytes(f"Conexion con servidor establecida!","utf-8"))

while True:
    #Recibo el mensaje del cliente, tambien declaro el tamaño del buffer (1024)
    mensaje = client_socket.recv(1024).decode('utf-8')
    client_socket.send(invertString(mensaje).encode('utf-8'))
