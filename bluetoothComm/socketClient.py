"""
A simple Python script to send messages to a sever over Bluetooth
using PyBluez (with Python 2).
"""

import bluetooth

serverMACAddress = '5C:F3:70:76:B6:5E'
port = 3
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMACAddress, port))
while 1:
    text = input()
    if text == "quit":
   		break
    s.send(text)
sock.close()