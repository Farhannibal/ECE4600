import bluetooth
from commandList import listOfCommand
from threading import Thread
from socketserver import ThreadingMixIn

hostMACAddress = '5C:F3:70:76:B6:5E'
port = 3
backlog = 1
dataSize = 1024

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
		client.send("ACK4S")
		serverDataRecv = client.recv(dataSize)
		serverDataRecv = serverDataRecv.decode("utf-8")

		# Second ACK the connection from client
		if listOfCommand(serverDataRecv) == 1:
			print("Connection established")
			while 1:
				# After establish connection, now start command client
				data = input()
				if listOfCommand(data) != 99:
					# If data is valid then start sending

					client.send(data)

					# Waiting for ACK signal
					serverDataRecv = client.recv(dataSize).decode("utf-8")

					# If ACK then keep going, if not resend data
					if listOfCommand(serverDataRecv) != 1:
						client.send(data)

					# if more than this point, give up on sending that --
					#  think more

					# Quit when user type quit in command line
					if data == "QUIT":
						break
				else:
					print("Wrong command, please check the command list and repeat input !")

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
		print("Closing socket")
		# close both client and server
		client.close()

for t in threads:
		t.join()
btConnect.close()








