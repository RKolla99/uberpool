from socket import *



# server info
serverName = '192.168.43.179'
serverPort = 11000

# create client socket 
clientSocket = socket(AF_INET,SOCK_STREAM)
# create tcp connection with server 
clientSocket.connect((serverName,serverPort))

# Take input from user 
sentence = input("Input lowercase letter : ")
clientSocket.send(str.encode(sentence))

returnMessage = clientSocket.recv(1024)

print(returnMessage.decode())

clientSocket.close()

