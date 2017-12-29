import bluetooth
import json

# Library of command
def listOfCommand(command):
	return{
		"ACK4S":0,
		"ACK4C":1,
		"UP":2,
		"DOWN":3,
		"LEFT":4,
		"RIGHT":5,
		"STOP":6,
		"QUIT":98
	}.get(command, 99) # default will be WAIT


def toJSON(message):
    if type(message) is bytes:
        message = message.decode("utf-8")
    return json.dumps(message)

def fromJSON(message):
    if type(message) is bytes:
        message = message.decode("utf-8")
    return json.loads(message)

# Definition of some basic data and address
hostMACAddress = '5C:F3:70:76:B6:5E'  # The MAC address of a Bluetooth adapter

# on the server. The server might have
# multiple Bluetooth adapters.
port = 3
backlog = 1
dataSize = 1024

# Establish connection between server and client
btConnect = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
btConnect.bind((hostMACAddress, port))
btConnect.listen(backlog)
print("Server is up !")
print("Waiting for connection ... ")

try:
    client, clientInfo = btConnect.accept()  # connect with client

    # First check if client finish estasblishing connection
    client.send("ACK4S")
    serverDataRecv = client.recv(dataSize).decode("utf-8")

    # Second ACK the connection from client
    if listOfCommand(serverDataRecv) == 1:
        print("Connection established")
        while 1:
            print("Please enter command (UP, DOWN, LEFT, RIGHT, STOP or QUIT): ")
            # After establish connection, now start command client
            data = input()
            if listOfCommand(data) != 99:
            # If data is valid then start sending

                client.send(data)
                # Waiting for update on position
                serverDataRecv = client.recv(dataSize).decode("utf-8")
                print(serverDataRecv)


                #Wait till the car is reaching their final destination


                # Quit when user type quit in command line
                if data == "QUIT":
                    break
            else:
                print("Wrong command, please check the command list and repeat input !")
except:
    print("Closing socket")
    # close both client and server
    client.close()

    #Finish the program
    btConnect.close()
