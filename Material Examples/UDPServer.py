from socket import *

serverPort = 12000

# SOCK_DGRAM establece como protocolo a UDP
# AF_INET establece como protocolo a IP
serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('127.0.0.1', 12001))

print("The server is ready to receive")

while 1:
	message, clientAddress = serverSocket.recvfrom(2048)
	#clienteAddres = (dir_ip, dir_puerto)
	print("mensaje: " + message.decode() + " recibido de direccion: " + clientAddress[0] + " y puerto: " + str(clientAddress[1]))
	modifiedMessage = message.decode().upper()
	serverSocket.sendto(modifiedMessage.encode(), clientAddress)