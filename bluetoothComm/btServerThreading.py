import bluetooth
from commandList import listOfCommand
from threading import Thread
from socketserver import ThreadingMixIn


class ClientThread(Thread):
	#	Override the __init(self[,args]) method to add
	#	additional arguments
	def __init__(self, address, port):
		Thread.__init(self)
		self.address = address
		self.port = port
		print ("* New server connection started for " + address +
		 " : " + str(port))

	#	Override the run(self[,args]) method to implement what
	#		the thread should do when started
	def run(self):
		while 1:
			text = input()
			# Quit when user type quit in command line
			btConnect.send(text) # close both client and server
			if text == "quit":
				break

# Definition of some basic data and address
hostMACAddress = "5C:F3:70:76:B6:5E" # The MAC address of a Bluetooth adapter 
					#on the server. The server might have 
					#multiple Bluetooth adapters.
bluetoothPort = 3
backlog = 1
size = 1024

btConnect = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
btConnect.bind((hostMACAddress, bluetoothPort))
btConnect.listen(backlog)
threads = []

while 1:
	try:
		client, (clientAddress, clientPort) = btConnect.accept()
		newthread = ClientThread(clientAddress, clientPort)
		newthread.start()
		threads.append(newthread)
	except:
		print("Failed to connect to client")
		client.close()
	btConnect.close()

for t in threads:
		t.join()








