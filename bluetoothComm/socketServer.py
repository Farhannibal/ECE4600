"""
A simple Python script to receive messages from a client over
Bluetooth using PyBluez.
"""

import bluetooth
from commandList import listOfCommand

# Definition of some basic data and address
hostMACAddress = '5C:F3:70:76:B6:5E' # The MAC address of a Bluetooth adapter 
					#on the server. The server might have 
					#multiple Bluetooth adapters.
port = 3
backlog = 1

# Establish connection between server and client
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
while 1:
   	text = input()
   	# Quit when user type quit in command line
   	s.send(text) # close both client and server 
   	if text == "quit":
  		break

s.close()