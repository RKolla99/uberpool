from socket import *

serverPort = 11000
serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind(('',serverPort))

serverSocket.listen(1)
print("The server is ready to recieve ")
while(1):
    connectionSocket,addr = serverSocket.accept()
    inputMessage = connectionSocket.recv(1024)
    print(inputMessage.decode())
    returnMessage = input("Reply to friend : ")
    connectionSocket.send(str.encode(returnMessage))
    connectionSocket.close()
