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

try:
	print("Connection established")
	while 1:
		data = s.recv(size)
		output_file.write(data)
		if data == "quit":
			print("Closing server ...")
			break
		elif listOfCommand(data) == 1:
			print("Go up")
		elif listOfCommand(data) == 2:
			print("Go back")
		elif listOfCommand(data) == 3:
			print("Turn left")
		elif listOfCommand(data) == 4:
			print("Turn right")
		elif listOfCommand(data) == 5:
			print("Stop the car!")
		else:
			print("Command is not available")
			client.send(data) # Echo back to client

	s.close() # When the server close the socket     
except:
	print("Error connecting to host")

output_file.close()