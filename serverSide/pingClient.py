import bluetooth
import time
from threading import Thread
import json
from pathlib import Path

# Library of command
def listOfCommand(command):
	return{
		"ACK4S":0,
		"ACK4C":1,
		"FORWARD":2,
		"BACK":3,
		"LEFT":4,
		"RIGHT":5,
		"STOP":6,
        "UPDATE":7,
		"QUIT":98,
        "WAIT":99
	}.get(command, 100) # default will be ERROR

def namesOfCars(MACAddress):
    return{
        "34:C3:D2:BF:1D:1A":"bigPine",
        "34:C3:D2:C2:86:17":"Pen",
        "34:C3:D2:C0:0E:6D":"Pineapple",
        "34:C3:D2:F8:C9:50":"Apple",
        "34:C3:D2:F8:D6:D1":"Hoodie",
        }.get(MACAddress, "nosupport")


class ThreadedServer(Thread):
    def __init__(self, hostMAC, port):
        #Thread.__init__(self)
        self.hostMAC = hostMAC
        self.port = port
        self.btConnect = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.btConnect.bind((hostMACAddress, port))
        print("Server is up!")

    def listen(self):
        backlog = 5
        print("Waiting for connection ... ")
        self.btConnect.listen(backlog)
        while True:
            client, address = self.btConnect.accept()
            #client.settimeout(60)
            Thread(target = self.listenToClient, args = (client, address)).start()

    # Method to establish the new connection for each thread
    def listenToClient(self, client, clientInfo):
        dataSize = 1024
         # First check if client is in our support
        clientName = namesOfCars(str(clientInfo[0]))

        # Reject if it's not in the system
        if (clientName =="nosupport"):
            client.close()
        else :
             # Check if client finish estasblishing connection
            client.send("ACK4S")
            serverDataRecv = client.recv(dataSize)
            serverDataRecv = serverDataRecv.decode("utf-8")
            
            # Second ACK the connection from client
            if listOfCommand(serverDataRecv) == 1:
                print("Connection established for "+clientName)
                print("Start ping the client")
                successPacketTransfer = 0
                data="ACK4S"
                # After establish connection, now start command client
                for x in range(0,5):
                        start = time.time()
                        client.send(data)
                        # Waiting for update on position
                        serverDataRecv = client.recv(dataSize).decode("utf-8")
                        end = time.time()
                        if listOfCommand(serverDataRecv) == 1: 
                            print("Successfully ping "+clientName+" in "+ str(end-start))
                            successPacketTransfer = successPacketTransfer+1
                            time.sleep(1)
                        else:
                            print("Unsuccessful ping, please restart the connection")
                            break
                print("Finish ping program. Number of successful transfer:"+ str(successPacketTransfer)+" out of 5")
                client.close()
        return False

if __name__ == "__main__":
    # Multithreaded Python server: Bluetooth server
    hostMACAddress = '00:1A:7D:DA:71:13' # Huy Bluetooth
    #hostMACAddress = '60:6C:66:B5:63:D1' # Aleksa Bluetooth
    btPort = 3  # default for pyBluez bluetooth

    newthread = ThreadedServer(hostMACAddress, btPort)
    newthread.listen()
