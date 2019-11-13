import socket
import select
import errno
import sys
import threading 


HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

my_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((IP,PORT))
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)


sendMessageActive = 0
getMessageActive = 0

clientStates = ['welcome','DriverorClient','Location input',"clientWait",'MakeDriverAvailable','DriverResponse','Confirm']

currentState = 'welcome'

print('Welcome To Uber')

def getMessage():

    global getMessageActive
    global currentState

    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
           
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")
           
            message_header = client_socket.recv(HEADER_LENGTH)
           
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")

            

            dataRecieved = (message).split(",")
            # print(f"{username} > {message}")
            if(currentState=="MakeDriverAvailable"):
                message = f"Client at {dataRecieved[2]} wants to go to {dataRecieved[3]}\nEnter 1 to accept and 0 to reject"
                print(message)
                currentState="DriverResponse"
            elif(currentState=="clientWait"):
                if(dataRecieved[0] == "1"):
                    print(f"{dataRecieved[1]} will pick you up shortly")
                else:
                    print("No driver available , please try again later")

    except IOError as e:
        # If there is nothing left to read then just continue
        if(e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK):
            print('Reading error',str(e))
        

    except Exception as e:
        print('General error',str(e))
        sys.exit()

    getMessageActive = 0
def sendMessage():

    global sendMessageActive
    global currentState

    if(currentState == 'welcome'):
        print('Enter 1 for client and 0 for driver')
        choice = int(input())
        if(choice != 1):
            currentState = 'MakeDriverAvailable'
        else:
            currentState = 'Location input'
    elif(currentState == 'Location input'):
        print("Enter pickup point")
        src = input()
        print("Enter destination point")
        dst = input()

        if(src and dst):
            # format - typeofrequest,ClientId,Src,Dst
            # 1 - booking request
            # 2 - End trip
            message = "1"+","+"1"+","+src+","+dst
            message = message.encode("utf-8")
            message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
            client_socket.send(message_header + message)
        
            print("Searching for a driver nearby...")
            currentState = "clientWait"
    elif(currentState=="DriverResponse"):
        response = int(input())
        code = 3
        if(response == 0):
            code = 4
        message = str(code)+","+"1"
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)
        
    # else:
    #     message = input(f"{my_username} > ")

    #     if(message):
    #         message = message.encode("utf-8")
    #         message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
    #         print(message_header)
    #         print(message_header + message)
    #         client_socket.send(message_header + message)
    sendMessageActive = 0

while True:
    if(not sendMessageActive):
        sendMessageActive = 1
        sendMsgThread = threading.Thread(target=sendMessage)
        sendMsgThread.start()
    
    if(not getMessageActive):
        getMessageActive = 1
        getMsgThread = threading.Thread(target=getMessage)
        getMsgThread.start()

    


        

    
        
