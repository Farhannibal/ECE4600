import bluetooth

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
    serverDataRecv = client.recv(dataSize)
    serverDataRecv = serverDataRecv.decode("utf-8")

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

                # Waiting for ACK signal
                serverDataRecv = client.recv(dataSize).decode("utf-8")

                # If ACK then keep going, if not resend data
                if listOfCommand(serverDataRecv) != 1 :
                    client.send(data)

                # if more than this point, give up on sending that --
                #  think more

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
