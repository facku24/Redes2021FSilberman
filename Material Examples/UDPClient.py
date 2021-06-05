from socket import *

serverName = 'locahost' #127.0.0.1
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

clientSocket.bind(('127.0.0.1', serverPort))

message = input('Input lowercase sentence:')

clientSocket.sendto(message.encode(), ('127.0.0.1', 12001))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

print(modifiedMessage.decode())

clientSocket.close()