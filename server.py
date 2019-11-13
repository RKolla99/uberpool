import socket
import select
from graphModule import *

# Graph setup

g = Graph(9) 
g.graph = [ [0, 4, 0, 0, 0, 0, 0, 8, 0], 
            [4, 0, 8, 0, 0, 0, 0, 11, 0], 
            [0, 8, 0, 7, 0, 4, 0, 0, 2], 
            [0, 0, 7, 0, 9, 14, 0, 0, 0], 
            [0, 0, 0, 9, 0, 10, 0, 0, 0], 
            [0, 0, 4, 14, 10, 0, 2, 0, 0], 
            [0, 0, 0, 0, 0, 2, 0, 1, 6], 
            [8, 11, 0, 0, 0, 0, 1, 0, 7], 
            [0, 0, 2, 0, 0, 0, 6, 7, 0] 
            ]; 

# Initial user and driver setup
g.addDriver("Ramesh",2,5)
g.addDriver("Suresh",7,5)

cli1 = Client("Ishar",1)
cli2 = Client("Menon",2) 

myUber = Uber(g)
myUber.addClient(cli1,cli1.clientId)
myUber.addClient(cli2,cli2.clientId)



HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234


server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

server_socket.bind((IP,PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False
        message_length = int(message_header.decode("utf-8").strip())
        return {"header":message_header,"data":client_socket.recv(message_length)}


    except:
        return False


while True:
    read_sockets,_,exception_sokcets = select.select(sockets_list,[],sockets_list)

    for notified_socket in read_sockets:
        
        # set up the tcp connection if not connected and store the username and socket info
        if notified_socket == server_socket:
            client_socket,client_address = server_socket.accept()

            user = receive_message(client_socket)
            
            if(user == False):
                continue
            sockets_list.append(client_socket)

            clients[client_socket] = user

            print(f"Accepted new connection from {client_address[0]} : {client_address[1]} username : {user['data'].decode('utf-8')}")
            # print("new connection made")
        # accept message if tcp connection already made and recieve the message and broadcast to all other users
        else:

            message = receive_message(notified_socket)

            if(message is False):
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]

            print(f"Recieved message from {user['data'].decode('utf-8')} : {message['data'].decode('utf-8')}")

            dataRecieved = list(map(int,(message['data'].decode('utf-8')).split(",")))

            print(dataRecieved)

            # Client waiting for the driver, look for nearest driver and send request to driver 
            if(dataRecieved[0] == 1):
                myUber.scheduleAndStartJourney(dataRecieved[2],dataRecieved[3],dataRecieved[1])

            # Driver has accepted the request
            elif(dataRecieved[0] == 3):
                clientID = dataRecieved[1]
                journeyId = myUber.clientInfo[clientID].journeys[-1]
                DriverIndex = myUber.journey[journeyId][1]
                DriverName = myUber.graph.driverInfo[DriverIndex].name
                responseMessage = "1"+","+DriverName
                message['data'] = (responseMessage).encode("utf-8")
                message['header'] = f"{len(responseMessage) :< {HEADER_LENGTH}}".encode("utf-8")
            # Driver has rejected the request
            elif(dataRecieved[0] == 4):
                myUber.cancelBooking(dataRecieved[1])
                responseMessage = "0"+","+"No Driver available"
                message['data'] = (responseMessage).encode("utf-8")
                message['header'] = f"{len(responseMessage) :< {HEADER_LENGTH}}".encode("utf-8")
            print(message['data'])
            print(user['header'] + user['data'] + message['header'] + message['data'])
            for client_socket in clients:
                if(client_socket  != notified_socket):
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                    
    
    for notified_socket in exception_sokcets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]