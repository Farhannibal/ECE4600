"""
	A simple Python script to receivee messages from a client
	over Bluetooth using Python sockets (with Python 3.3 or above)

"""
import socket

hostMACAddress='00:1f:e1:dd:08:3d'
port = 3
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM,
 socket.BTPROTO_RFCOMM)
s.bind(hostMACAddress, port)
s.listen(backlog)
try:
	client, address = s.accept()
	while 1:
		data = client.recv(size)
		if data:
			print(data)
			client.send(data)
except:
	print("Closing socket")
	client.close()
	s.close()
	
