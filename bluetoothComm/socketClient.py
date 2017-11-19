"""
A simple Python script to send messages to a sever over Bluetooth
using PyBluez
"""

import bluetooth
from commandList import listOfCommand

serverMACAddress = '5C:F3:70:76:B6:5E'
port = 3
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
output_file = open("CommandQueue.txt", "w")
size = 1024

# Establish connection between server and client
s.connect((serverMACAddress, port))

clientRecvData = s.recv(size)
clientRecvData = clientRecvData.decode("utf-8")

if listOfCommand(clientRecvData) == 0:
    s.send("ACK4C")
    print("Connection established")
    # Write the END of the Queue to the file
    output_file.write("END"+"\n")
    while 1:
        # Keep listening from Server
        clientRecvData = s.recv(size)
        clientRecvData = clientRecvData.decode("utf-8")

        # Error detection:
        if listOfCommand(clientRecvData) == 99:
            print("Received error message, need send back new command!")
        # Else there is no error:
        else:

            # Quit when server decide to quit
            if clientRecvData == "QUIT":
                break
            # Else follow the command
            elif listOfCommand(clientRecvData) == 2:
                print("Go up")
            elif listOfCommand(clientRecvData) == 3:
                print("Go back")
            elif listOfCommand(clientRecvData) == 4:
                print("Turn left")
            elif listOfCommand(clientRecvData) == 5:
                print("Turn right")
            elif listOfCommand(clientRecvData) == 6:
                print("Stop the car!")

            # Send ACK back
            s.send("ACK4C")
            output_file.write(clientRecvData + "\n")


print("Cut connection")


    # output_file.write(data.decode("utf-8"))

    # if data == "quit":
    #     print("Closing server ...")
    #     break
    # # elif listOfCommand(data) == 0:
    # #     s.send("ACK4C")
    #
    # else:
    #     print("Command is not available")
    #     #s.send(data)  # Echo back to client

s.close()  # When the server close the socket

# print("Error connecting to host")

output_file.close()
