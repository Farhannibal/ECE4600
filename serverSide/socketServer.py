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

# Definition of some basic data and address
#hostMACAddress = '60:6c:66:b5:63:d1'  # Farhan bluetooth adapter
#hostMACAddress = '5C:F3:70:76:B6:5E' # My bluetooth adapter
SERVER_MAC_ADDRESS = '60:6C:66:B5:63:D1' # Aleksa bluetooth
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
    serverDataRecv = client.recv(dataSize)
    serverDataRecv = serverDataRecv.decode("utf-8")

    #control = 0
    control = 2

    counter = 1
    queue = []

    # Second ACK the connection from client
    if listOfCommand(serverDataRecv) == 1:
        print("Connection established")
        while 1:
            # After establish connection, now start command client
            if control == 0:
                queue = str(json.load(open("Traffic_Sim/Assets/CarData.json"))["commands"]).split(',')
                control = 1
                data = queue[0]
            elif len(queue) > counter:
                data = queue[counter]
                counter = counter + 1
            else:
                print("Please enter command (UP, DOWN, LEFT, RIGHT, STOP or QUIT): ")
                data = input()

            if listOfCommand(data) != 99:
            # If data is valid then start sending

                client.send(data)
                    
                # Waiting for update on position
                serverDataRecv = client.recv(dataSize).decode("utf-8")
                print(serverDataRecv)
                with open('Traffic_Sim/Assets/data.json', 'w') as outfile:
                #with open('data.json', 'w') as outfile:
                    outfile.write(serverDataRecv)
                # Quit when user type quit in command line
                if data == "QUIT":
                    break
            else:
                print("Wrong command, please check the command list and repeat input !")
except Exception as e:
    print("Closing socket")
    print(e)
    # close both client and server
    client.send("QUIT")
    client.close()

    #Finish the program
    btConnect.close()